#!/bin/sh

echo "Pipeline execution started"
python ./data/pipeline.py
echo "Execution Completed"

echo "Test started"
python ./data/test.py
echo "Test ended"
