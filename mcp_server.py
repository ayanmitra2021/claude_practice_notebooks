from pydantic import Field

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system and nothing else.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the content of a document and return its content as a string"
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Document with doc id {doc_id} not found")
    
    return docs[doc_id]
    
# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_doc_content",
    description="Edits the content of a document by replacing the string in the document with a new string"
)
def edit_document(
    doc_id: str = Field(description="Id of the document to be edited"),
    old_string: str = Field(description="The old string which has to be replaced in the document"),
    new_string: str = Field(description="The new string which will replace the old string")
):
    if doc_id not in docs:
        raise ValueError(f"Document with doc id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_string, new_string)

@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with doc id {doc_id} not found")
    
    return docs[doc_id]
    

@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in a Markdown format"
)
def format_document(
    doc_id: str= Field(description="Id of the document being formatted")
):
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:

{doc_id}


Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra formatting.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""
    
    return [
        base.UserMessage(prompt)
    ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
