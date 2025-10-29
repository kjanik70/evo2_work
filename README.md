# Genetics Analysis Workspace

This workspace is set up for genetics and bioinformatics analysis using Python with GPU acceleration via NVIDIA's PyTorch container.

## Project Structure

- `data/`: Store your genetic data files
- `scripts/`: Python scripts for data analysis
- `notebooks/`: Jupyter notebooks for interactive analysis
- `tests/`: Unit tests for your code

## Setup Instructions using NVIDIA PyTorch Container

### Important: Use WSL Terminal Directly

To maintain a stable container session, always use the WSL terminal directly instead of letting VS Code or other tools open PowerShell terminals. This prevents getting kicked out of the container.

1. Open WSL terminal manually (do not use VS Code's terminal):
```bash
wsl
```

2. Navigate to the workspace:
```bash
cd /mnt/c/Users/kjani/OneDrive/Documents/OSU\ Genomics/Genomics_Workspace
```

3. Pull the latest NVIDIA PyTorch container:
```bash
docker pull nvcr.io/nvidia/pytorch:25.09-py3
```

4. Run the container with GPU support and mount the workspace:
```bash
docker run --gpus all -it --rm \
  -p 8889:8888 \
  -v "$PWD":/workspace \
  nvcr.io/nvidia/pytorch:25.09-py3
```

5. Inside the container, set up Jupyter and required packages:
```bash
# Install required packages
pip install jupyter notebook ipykernel biopython scikit-learn statsmodels seaborn

# Register the kernel
python -m ipykernel install --user --name=pytorch-gpu --display-name "Python (PyTorch GPU)"

# Start Jupyter (keep this running)
jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root --notebook-dir=/workspace
```

### Accessing Jupyter Notebook

1. When Jupyter starts, copy the URL with token from the terminal
2. Access the notebook in your browser at `http://127.0.0.1:8889` (note the port change from 8888 to 8889)

### Port Mapping Explanation

- Inside container: Jupyter runs on port 8888
- On host machine: Access through port 8889 (mapped via Docker)

### Restarting the Environment

If you need to restart:

1. Keep the WSL terminal open at all times
2. If you exit the container, just run the `docker run` command again
3. If you close the WSL terminal, start fresh from step 1 of the setup instructions

Note: The PyTorch container comes with numpy, pandas, matplotlib, and other ML libraries pre-installed. The additional packages we install are specifically for genomics analysis.

Note: When working with large genomic datasets, you might experience slightly slower I/O performance when accessing files on the Windows filesystem through WSL2. This is normal and usually acceptable for most analyses.

## Getting Started

1. Launch Jupyter from within the container:
```bash
jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root --notebook-dir=/workspace
```

2. Copy the URL with token that appears in the terminal and paste it into your browser.

3. Navigate to the `notebooks` directory to open the `genetics_starter.ipynb` notebook.

## Using GPU Acceleration

The container comes with PyTorch pre-configured for GPU usage. To verify GPU access:

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
```

## Container Management

- To exit the container:
```bash
exit
```

- To restart later, run the docker run command from step 2 again.
- Your work will be preserved in the mounted workspace directory.

## Dependencies

See `requirements.txt` for a full list of Python packages.

## EVO2 Genome Prediction Notebook

A new notebook, `notebooks/evo2_predictions.ipynb`, demonstrates how to:
- Read a genome FASTA file from the `data/` directory
- Query the NVIDIA EVO2 model for sequence predictions at various input sizes (128 to 1,048,576 bases)
- Compare the model's generated output to the next 128 bases in the genome
- Save results to `results/evo2_predictions_results.csv`

### Running the EVO2 Notebook

1. Place your genome FASTA file(s) in the `data/` directory.
2. Open the notebook in Jupyter: `notebooks/evo2_predictions.ipynb`
3. When prompted, provide your `NVCF_RUN_KEY` (or set it as an environment variable before starting Jupyter).
4. Run all cells. Results will be saved in the `results/` directory.

**Chunking for Large Inputs:**
- The notebook automatically splits very large input sequences into manageable chunks if the EVO2 API or service has input size limits. Results are aggregated for comparison.
- You can adjust the chunk size in the notebook if needed for your API quota or service limits.

See the notebook for more details and example code.

## EVO2 Model Timeout (NIM_EVO2_TIMEOUT_S)

If you encounter errors like:

    HTTP 422 response body: ... "Timed out on ...th token. Allowed to run for 120 seconds. You can change the limit by setting NIM_EVO2_TIMEOUT_S environment variable."

This means the EVO2 model server timed out while processing your request. You can increase the allowed runtime for long requests by setting the `NIM_EVO2_TIMEOUT_S` environment variable before starting the service (if you control the deployment):

```bash
# Example: allow up to 10 minutes (600 seconds) per request
export NIM_EVO2_TIMEOUT_S=600
```

If you are using the public NVIDIA endpoint, you may not be able to change this limit. In that case, reduce your input size or chunk size in the notebook to avoid timeouts.