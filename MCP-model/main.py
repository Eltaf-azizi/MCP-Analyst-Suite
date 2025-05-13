from fastmcp import FastMCP
from tools.mcp_swot import test_api_endpoint


mcp = FastMCP("swot analysis mcp")

@mcp.tool()
def swot_analysis():
    return test_api_endpoint()


if __name__ == "__main__":
    mcp.run()
