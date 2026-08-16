.PHONY: dashboard

dashboard:
	@echo "🚀 QuantAINexus Dashboard running at http://localhost:8765"
	@cd ../frontend && python3 -m http.server 8765
