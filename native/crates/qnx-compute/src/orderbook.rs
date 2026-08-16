use pyo3::prelude::*;
use std::collections::{BTreeMap, VecDeque};

#[derive(Clone, Debug)]
pub struct Order {
    pub id: u64,
    pub price: u64, // Scaled by 10000 to avoid float issues
    pub qty: f64,
    pub side: bool, // true for bid, false for ask
}

#[derive(Clone, Debug)]
#[pyclass]
pub struct Fill {
    #[pyo3(get)]
    pub order_id: u64,
    #[pyo3(get)]
    pub match_price: f64,
    #[pyo3(get)]
    pub match_qty: f64,
}

#[pyclass]
pub struct OrderbookMatcher {
    bids: BTreeMap<u64, VecDeque<Order>>,
    asks: BTreeMap<u64, VecDeque<Order>>,
    next_id: u64,
    scale: f64, // 10000.0
}

#[pymethods]
impl OrderbookMatcher {
    #[new]
    pub fn new() -> Self {
        OrderbookMatcher {
            bids: BTreeMap::new(),
            asks: BTreeMap::new(),
            next_id: 1,
            scale: 10000.0,
        }
    }

    /// Add an order to the book. Returns the order ID.
    pub fn add_order(&mut self, price: f64, qty: f64, is_bid: bool) -> PyResult<u64> {
        let id = self.next_id;
        self.next_id += 1;
        
        let scaled_price = (price * self.scale).round() as u64;
        let order = Order {
            id,
            price: scaled_price,
            qty,
            side: is_bid,
        };
        
        if is_bid {
            self.bids.entry(scaled_price).or_insert_with(VecDeque::new).push_back(order);
        } else {
            self.asks.entry(scaled_price).or_insert_with(VecDeque::new).push_back(order);
        }
        
        Ok(id)
    }

    /// Process a market tick and return any fills
    pub fn process_tick(&mut self, bid_price: f64, ask_price: f64) -> PyResult<Vec<Fill>> {
        let mut fills = Vec::new();
        
        let scaled_bid = (bid_price * self.scale).round() as u64;
        let scaled_ask = (ask_price * self.scale).round() as u64;
        
        // Match resting bids against the new market ask
        let mut bids_to_remove = Vec::new();
        for (&price, orders) in self.bids.iter_mut().rev() {
            if price >= scaled_ask {
                for order in orders.iter_mut() {
                    fills.push(Fill {
                        order_id: order.id,
                        match_price: ask_price, // Matched at the market ask
                        match_qty: order.qty,
                    });
                }
                bids_to_remove.push(price);
            } else {
                break; // Since we iterate rev(), once price < scaled_ask, no further matches
            }
        }
        for price in bids_to_remove {
            self.bids.remove(&price);
        }
        
        // Match resting asks against the new market bid
        let mut asks_to_remove = Vec::new();
        for (&price, orders) in self.asks.iter_mut() {
            if price <= scaled_bid {
                for order in orders.iter_mut() {
                    fills.push(Fill {
                        order_id: order.id,
                        match_price: bid_price, // Matched at the market bid
                        match_qty: order.qty,
                    });
                }
                asks_to_remove.push(price);
            } else {
                break; // Since we iterate forward, once price > scaled_bid, no further matches
            }
        }
        for price in asks_to_remove {
            self.asks.remove(&price);
        }
        
        Ok(fills)
    }

    pub fn best_bid_ask(&self) -> PyResult<(Option<f64>, Option<f64>)> {
        let best_bid = self.bids.keys().rev().next().map(|&p| (p as f64) / self.scale);
        let best_ask = self.asks.keys().next().map(|&p| (p as f64) / self.scale);
        Ok((best_bid, best_ask))
    }
}
