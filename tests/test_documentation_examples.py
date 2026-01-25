"""
ドキュメント内のコード例の実行可能性をテスト

このテストは、docs/api/ 内の各Markdownファイルからコード例を抽出し、
構文エラーがないことを確認します。
"""

import ast
import re
from pathlib import Path

import pytest


def extract_python_code_blocks(md_file: Path) -> list[tuple[int, str]]:
    """
    Markdownファイルからpythonコードブロックを抽出

    Returns:
        List of (block_number, code) tuples
    """
    content = md_file.read_text(encoding="utf-8")
    pattern = r"```python\s*\n(.*?)\n\s*```"
    matches = re.findall(pattern, content, re.DOTALL)
    return [(i + 1, code) for i, code in enumerate(matches)]


def get_all_markdown_files() -> list[Path]:
    """docs/api/ 内の全Markdownファイルを取得"""
    docs_dir = Path(__file__).parent.parent / "docs" / "api"
    if not docs_dir.exists():
        return []
    return list(docs_dir.rglob("*.md"))


@pytest.mark.parametrize("md_file", get_all_markdown_files())
def test_documentation_code_syntax(md_file: Path):
    """ドキュメント内のコード例が構文的に正しいことを確認"""
    code_blocks = extract_python_code_blocks(md_file)

    if not code_blocks:
        pytest.skip(f"No Python code blocks found in {md_file.name}")

    errors = []
    for block_num, code in code_blocks:
        try:
            # 構文チェックのみ（実行はしない）
            ast.parse(code)
        except SyntaxError as e:
            errors.append(
                f"Code block {block_num} has syntax error at line {e.lineno}: {e.msg}"
            )

    assert not errors, f"\n{md_file.name}:\n" + "\n".join(
        f"  - {err}" for err in errors
    )


def test_all_documentation_files_exist():
    """APIドキュメントファイルが存在することを確認"""
    expected_files = [
        "portfolio/balances.md",
        "portfolio/positions.md",
        "trading/orders.md",
        "trading/prices.md",
        "referencedata/instruments.md",
        "rootservices/subscriptions.md",
        "rootservices/user.md",
        "chart/charts.md",
        "eventnotificationservices/clientactivities.md",
        "valueadd/pricealerts.md",
    ]

    docs_dir = Path(__file__).parent.parent / "docs" / "api"
    missing = []

    for expected in expected_files:
        file_path = docs_dir / expected
        if not file_path.exists():
            missing.append(expected)

    assert not missing, f"Missing documentation files: {', '.join(missing)}"


def test_code_blocks_have_imports():
    """コード例が必要なimport文を含むことを確認"""
    docs_dir = Path(__file__).parent.parent / "docs" / "api"

    for md_file in docs_dir.rglob("*.md"):
        code_blocks = extract_python_code_blocks(md_file)

        for block_num, code in code_blocks:
            # 実際にsaxo_openapiを使用している場合のみチェック
            # コメントのみや設定例はスキップ
            code_stripped = code.strip()
            if not code_stripped or code_stripped.startswith("#"):
                continue

            # saxo_openapi の使用を検出
            if any(keyword in code for keyword in ["Client", "endpoints", "saxo"]):
                if "saxo_openapi" not in code:
                    pytest.fail(
                        f"{md_file.name}: Code block {block_num} "
                        f"uses saxo_openapi but does not import it"
                    )


if __name__ == "__main__":
    # 直接実行時のテスト
    pytest.main([__file__, "-v"])
