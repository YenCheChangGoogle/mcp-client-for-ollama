from fastmcp import FastMCP
from pydantic import BaseModel, validator
import asyncio
import os
from pathlib import Path

# 指定安全目錄
BASE_DIR = Path(r"C:\GIT\github\mcp-client-for-ollama.git\DEMO").resolve()

mcp = FastMCP("FileToolServer")

class FileCommand(BaseModel):
    input_path: str
    output_path: str
    prefix: str

    @validator("input_path", "output_path")
    def validate_path(cls, v):
        full_path = (BASE_DIR / v).resolve()
        if not str(full_path).startswith(str(BASE_DIR)):
            raise ValueError(f"路徑不在安全目錄內：{full_path}")
        return v

@mcp.tool()
def read_and_write_file(cmd: FileCommand) -> dict:
    input_file = (BASE_DIR / cmd.input_path).resolve()
    output_file = (BASE_DIR / cmd.output_path).resolve()

    if not input_file.exists():
        return {"status": "error", "message": f"找不到檔案：{input_file}"}

    try:
        
        #寫檔範例
        #with open(r"C:\GIT\github\mcp-client-for-ollama.git\DEMO\input.txt", "w", encoding="utf-8") as f:
        #    f.write("這是一段測試文字。")

        
        with input_file.open("r", encoding="utf-8") as f:
            content = f.read()

        processed = f"{cmd.prefix}{content}"

        with output_file.open("w", encoding="utf-8") as f:
            f.write(processed)

        return {
            "status": "success",
            "input_preview": content[:50],
            "output_path": str(output_file)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def main():
    await mcp.run_http_async(host="127.0.0.1", port=6274)

if __name__ == "__main__":
    asyncio.run(main())