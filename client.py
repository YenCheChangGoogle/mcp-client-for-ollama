import asyncio
from fastmcp import Client

async def main():
    server_url = "http://127.0.0.1:6274/mcp"
    print(f"🚀 連接 MCP 工具伺服器：{server_url}")

    client = Client(server_url)

    try:
        async with client:
            print("✅ MCP 客戶端初始化完成")

            # 🧰 列出工具
            tools = await client.list_tools()
            print("🧰 工具列表：")
            for tool in tools:
                print(f" - {tool.name}")

            # 🔧 呼叫工具：讀檔並寫檔
            print("\n🧪 呼叫 read_and_write_file 工具")
            result = await client.call_tool("read_and_write_file", {
                "cmd": {
                    "input_path": "input.txt",       # 相對於 DEMO 目錄
                    "output_path": "output.txt",
                    "prefix": "[處理後] "
                }
            })

            # 📦 顯示回傳結果
            print("\n📦 工具回傳內容：")
            for key, value in result.structured_content.items():
                print(f" - {key}: {value}")

    except Exception as e:
        import traceback
        print("❌ 發生錯誤：", repr(e))
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())