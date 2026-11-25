"""End-to-end smoke test: idalib-mcp via stdio, opens a real binary headless."""
import asyncio, json, sys

sys.path.insert(0, r"D:\TOOLS\IDA\mcp-venv\Lib\site-packages")

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MCP_CMD = r"D:\TOOLS\IDA\mcp-venv\Scripts\idalib-mcp.exe"
TARGET = sys.argv[1] if len(sys.argv) > 1 else r"C:\Windows\System32\hostname.exe"

async def main():
    params = StdioServerParameters(command=MCP_CMD, args=["--stdio"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = sorted(t.name for t in tools.tools)
            print(f"OK: {len(names)} tools exposed")
            print("sample:", names[:12])

            print(f"\n-> idb_open({TARGET}) ...")
            r = await session.call_tool("idb_open", {"input_path": TARGET})
            txt = " ".join(str(c.text) for c in r.content if getattr(c, "type", "") == "text")
            print("idb_open:", txt[:600])
            if "session" not in txt and '"' not in txt:
                print("WARNING: unexpected idb_open output")
                return

            print("\n-> idb_list ...")
            r = await session.call_tool("idb_list", {})
            txt = " ".join(str(c.text) for c in r.content if getattr(c, "type", "") == "text")
            print("idb_list:", txt[:400])

            # try to grab the session id from idb_open output (JSON)
            db = None
            try:
                parsed = json.loads(txt)
                if isinstance(parsed, dict):
                    db = parsed.get("session") or parsed.get("session_id")
                elif isinstance(parsed, list):
                    db = parsed[0].get("session")
            except Exception:
                pass

            if not db:
                # fallback: idb_list entries
                try:
                    parsed = json.loads(txt)
                    entries = parsed if isinstance(parsed, list) else parsed.get("sessions", [])
                    for e in entries:
                        if e.get("session"):
                            db = e["session"]; break
                except Exception:
                    pass
            print("db session:", db)

            if db:
                print("\n-> list_funcs (limit 5)...")
                r = await session.call_tool("list_funcs", {"queries": {"limit": 5}})
                txt = " ".join(str(c.text) for c in r.content if getattr(c, "type", "") == "text")
                print("list_funcs:", txt[:500])

                print("\n-> int_convert smoke test...")
                r = await session.call_tool("int_convert", {"inputs": {"0x401000": ["dec", "bytes"]}})
                txt = " ".join(str(c.text) for c in r.content if getattr(c, "type", "") == "text")
                print("int_convert:", txt[:300])

                print("\n-> idb_close (save=False)...")
                r = await session.call_tool("idb_close", {"database": db})
                txt = " ".join(str(c.text) for c in r.content if getattr(c, "type", "") == "text")
                print("idb_close:", txt[:200])

    print("\nSMOKE TEST COMPLETE")

asyncio.run(main())