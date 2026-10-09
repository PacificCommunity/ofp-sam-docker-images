"""Manual CPU-only localhost launcher; no downloads or automatic startup."""
import os

ARGV=['/opt/llama/llama-server','--model','/opt/kimsa/models/qwen3-0.6b.gguf','--host','127.0.0.1','--port','8080','--threads','2','--threads-batch','2','--parallel','1','--ctx-size','4096','--n-gpu-layers','0','--cache-ram','0','--cache-reuse','0','--offline','--no-warmup']

if __name__=='__main__':
    os.execve(ARGV[0],ARGV,dict(os.environ,LD_LIBRARY_PATH='/opt/llama'))
