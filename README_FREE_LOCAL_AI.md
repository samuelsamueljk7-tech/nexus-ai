# NEXUS — Free Local AI Edition (Mac)

This edition switches NEXUS's AI brain from the paid OpenAI API to Ollama running locally on your Mac. No OpenAI API key or API credits are needed. Internet is needed once to download Ollama/model; after the model is installed, prompts can run locally.

## One-time setup

1. Install Ollama for macOS from https://ollama.com/download and open the Ollama app.
2. Open Terminal in VS Code, inside this `pc controller` folder.
3. Download the default model (about a few GB):

   ```bash
   ollama pull qwen3:4b
   ```

4. Test it:

   ```bash
   ollama run qwen3:4b
   ```

   Type `Hello NEXUS`, make sure it answers, then type `/bye` to leave the model chat.

## Start NEXUS

Double-click `Launch Spark.command`, or in VS Code terminal run:

```bash
python3 start_spark_mac.py
```

The launcher creates `.spark-venv`, installs dependencies, starts NEXUS, and opens http://127.0.0.1:5000. If macOS blocks the `.command` file, use the terminal command above.

## If NEXUS cannot reach its local AI

- Open the Ollama app first.
- In Terminal, run `ollama list` and make sure `qwen3:4b` appears.
- If it is missing, run `ollama pull qwen3:4b`.
- Keep Ollama running while using Spark.

## Notes

- Default model: `qwen3:4b`. You can change it by setting `SPARK_MODEL` before launching, as long as that model is installed in Ollama.
- Local model speed depends on your Mac's RAM and chip. If it feels slow, choose a smaller Ollama model.
- NEXUS's login screen is a local UI gate, not a real account/password authentication service. Do not use it to protect sensitive data.
- The robot mouth animation and browser speech are UI effects; speech synthesis availability depends on your browser.
- No API key is needed. Avoid putting secrets in frontend files.
