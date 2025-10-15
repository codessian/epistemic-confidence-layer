.PHONY: demo evaluate

demo:
	uvicorn src.ecl.server.app:app --reload

evaluate:
	python benchmarks/scripts/plot_reliability.py --input benchmarks/tasks/toy.jsonl --output benchmarks/results/reliability.png
	@echo "Wrote benchmarks/results/reliability.png"