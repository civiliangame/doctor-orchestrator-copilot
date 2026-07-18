// Tiny markdown-ish renderer — just enough for the seeded documents and the
// compiled intake: **bold**, *italic*, pipe tables, headings, lists, paragraphs.
// No deps, no HTML injection (everything goes through React text nodes).

import type { ReactNode } from "react";

function inline(text: string, keyBase: string): ReactNode[] {
  // **bold** first, then *italic* inside the leftovers.
  const out: ReactNode[] = [];
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  parts.forEach((part, i) => {
    const key = `${keyBase}-${i}`;
    if (part.startsWith("**") && part.endsWith("**") && part.length > 4) {
      out.push(<strong key={key}>{part.slice(2, -2)}</strong>);
      return;
    }
    const italics = part.split(/(\*[^*\n]+\*)/g);
    italics.forEach((seg, j) => {
      const k = `${key}-${j}`;
      if (seg.startsWith("*") && seg.endsWith("*") && seg.length > 2) {
        out.push(<em key={k}>{seg.slice(1, -1)}</em>);
      } else if (seg) {
        out.push(<span key={k}>{seg}</span>);
      }
    });
  });
  return out;
}

function splitRow(line: string): string[] {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((c) => c.trim());
}

const isTableLine = (l: string) => /^\s*\|.*\|\s*$/.test(l);
const isDividerLine = (l: string) => /^\s*\|?[\s:|-]+\|?\s*$/.test(l) && l.includes("-");

export function Markdown({ text }: { text: string }) {
  const lines = (text ?? "").split(/\r?\n/);
  const blocks: ReactNode[] = [];
  let i = 0;
  let key = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (!line.trim()) {
      i++;
      continue;
    }

    // table
    if (isTableLine(line)) {
      const tableLines: string[] = [];
      while (i < lines.length && isTableLine(lines[i])) {
        tableLines.push(lines[i]);
        i++;
      }
      const header = splitRow(tableLines[0]);
      const bodyLines = tableLines.slice(1).filter((l) => !isDividerLine(l));
      blocks.push(
        <div className="md-table-wrap" key={key++}>
          <table className="md-table">
            <thead>
              <tr>
                {header.map((c, ci) => (
                  <th key={ci}>{inline(c, `h${ci}`)}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {bodyLines.map((l, ri) => (
                <tr key={ri}>
                  {splitRow(l).map((c, ci) => (
                    <td key={ci}>{inline(c, `r${ri}c${ci}`)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>,
      );
      continue;
    }

    // heading
    const h = /^(#{1,4})\s+(.*)$/.exec(line);
    if (h) {
      const level = h[1].length;
      const cls = `md-h md-h${level}`;
      blocks.push(
        <div className={cls} key={key++}>
          {inline(h[2], "h")}
        </div>,
      );
      i++;
      continue;
    }

    // list (unordered or ordered)
    if (/^\s*([-*]|\d+[.)])\s+/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\s*([-*]|\d+[.)])\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*([-*]|\d+[.)])\s+/, ""));
        i++;
      }
      blocks.push(
        <ul className="md-list" key={key++}>
          {items.map((it, ii) => (
            <li key={ii}>{inline(it, `li${ii}`)}</li>
          ))}
        </ul>,
      );
      continue;
    }

    // paragraph: gather until blank / structural line
    const para: string[] = [line];
    i++;
    while (
      i < lines.length &&
      lines[i].trim() &&
      !isTableLine(lines[i]) &&
      !/^(#{1,4})\s+/.test(lines[i]) &&
      !/^\s*([-*]|\d+[.)])\s+/.test(lines[i])
    ) {
      para.push(lines[i]);
      i++;
    }
    blocks.push(
      <p className="md-p" key={key++}>
        {inline(para.join(" "), "p")}
      </p>,
    );
  }

  return <div className="md">{blocks}</div>;
}
