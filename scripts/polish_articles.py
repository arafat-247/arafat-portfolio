"""Apply a stable editorial reading layout to every canonical story page."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

ARTICLE_CSS = r"""
/* Canonical article reading layout v18.10 */
body.inner main{
  background:#f7f3ea;
}
.articlepage{
  --article-accent:var(--section-accent,#b9563e);
  width:min(100% - 48px,940px)!important;
  max-width:940px!important;
  margin:0 auto;
  padding:38px 0 78px!important;
}
.articlehead{
  max-width:840px;
  margin:0 auto;
  padding:0 0 24px;
  border-bottom:1px solid #d9d2c6;
}
.articleback{
  display:inline-block;
  margin:0 0 18px;
  color:#70716c;
  font-size:11px;
  font-weight:700;
  text-decoration:none;
}
.articleback:hover{color:var(--article-accent)}
.articlekicker{
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  gap:7px;
  margin:0 0 10px;
  color:var(--article-accent);
  font-size:9px;
  font-weight:850;
  letter-spacing:.13em;
  text-transform:uppercase;
}
.articlecategory{color:#73736d;text-decoration:none}
.articlekicker-sep{color:#b8b1a5}
.articlehead h1{
  max-width:820px!important;
  margin:0!important;
  color:#171814;
  font:400 clamp(42px,5.4vw,68px)/.98 var(--serif)!important;
  letter-spacing:-.042em!important;
  text-wrap:balance;
}
.articlestandfirst{
  max-width:770px;
  margin:17px 0 0;
  color:#555850;
  font:400 19px/1.5 var(--reading-serif,Georgia,serif);
}
.articlemeta{
  display:grid;
  grid-template-columns:minmax(160px,1fr) auto auto;
  gap:18px;
  align-items:end;
  margin-top:23px;
}
.articlebyline strong{
  display:block;
  color:#22231f;
  font-size:13px;
  line-height:1.2;
}
.articlecredit{
  display:block;
  margin-top:4px;
  color:#767770;
  font-size:10px;
  line-height:1.35;
}
.articlefacts{
  display:flex;
  flex-wrap:wrap;
  justify-content:flex-end;
  gap:6px 10px;
  color:#72736d;
  font-size:9px;
  font-weight:800;
  letter-spacing:.055em;
  text-transform:uppercase;
}
.articlefacts span+span:before{
  content:"•";
  margin-right:10px;
  color:var(--article-accent);
}
.articleactions{
  display:flex;
  gap:6px;
}
.articleactions button{
  padding:7px 9px;
  border:1px solid #d6cfc3;
  color:#383a35;
  background:#fbf8f1;
  font-size:9px;
  font-weight:750;
  cursor:pointer;
}
.articleactions button:hover{
  border-color:var(--article-accent);
  color:var(--article-accent);
}
.articlebodywrap{
  max-width:720px;
  margin:30px auto 0;
}
.articlecover{
  margin:0 0 28px;
}
.articlecover img{
  display:block;
  width:100%;
  height:auto;
  max-height:none;
  object-fit:contain;
}
.articlecover figcaption{
  margin-top:7px;
  color:#777870;
  font-size:10px;
  line-height:1.45;
}
.articlebody{
  max-width:none!important;
  color:#22231f!important;
  font:400 19px/1.76 var(--reading-serif,Georgia,serif)!important;
  letter-spacing:-.004em;
}
.articlebody p{margin:0 0 1.4em}
.articlebody h2{
  margin:2em 0 .62em;
  font:600 30px/1.16 var(--reading-serif,Georgia,serif)!important;
}
.articlebody h3{
  margin:1.7em 0 .55em;
  font:600 23px/1.2 var(--reading-serif,Georgia,serif)!important;
}
.articlebody blockquote{
  margin:1.7em 0;
  padding:2px 0 2px 20px;
  border-left:3px solid var(--article-accent);
  color:#31332f;
  font:400 22px/1.52 var(--reading-serif,Georgia,serif)!important;
}
.articlebody img{
  display:block;
  max-width:100%;
  height:auto;
  margin:26px auto;
}
.articlesource{
  max-width:none!important;
  margin-top:34px!important;
  padding:15px 0!important;
  border:0!important;
  border-top:1px solid #d9d2c6!important;
  border-bottom:1px solid #d9d2c6!important;
  background:transparent!important;
  color:#666860;
  font-size:11px;
  line-height:1.5;
}
body.inner[data-section="reporting"] .articlepage{--article-accent:#b9563e}
body.inner[data-section="opinion"] .articlepage{--article-accent:#a88642}
body.inner[data-section="thoughts"] .articlepage{--article-accent:#b57943}

@media(max-width:800px){
  .articlepage{
    width:100%!important;
    padding:20px 18px 52px!important;
  }
  .articlehead{
    max-width:none;
    padding-bottom:18px;
  }
  .articleback{
    margin-bottom:13px;
    font-size:10px;
  }
  .articlekicker{
    margin-bottom:8px;
    font-size:8px;
  }
  .articlehead h1{
    max-width:none!important;
    font-size:clamp(33px,9.2vw,45px)!important;
    line-height:1.01!important;
    letter-spacing:-.036em!important;
  }
  .articlestandfirst{
    max-width:none;
    margin-top:12px;
    font-size:16px;
    line-height:1.48;
  }
  .articlemeta{
    grid-template-columns:1fr auto;
    gap:12px 14px;
    margin-top:17px;
  }
  .articlefacts{
    grid-column:1/-1;
    grid-row:2;
    justify-content:flex-start;
    padding-top:9px;
    border-top:1px solid #ddd6ca;
    font-size:8px;
  }
  .articleactions{justify-content:flex-end}
  .articlebodywrap{
    max-width:none;
    margin-top:22px;
  }
  .articlebody{
    font-size:17.5px!important;
    line-height:1.72!important;
  }
  .articlebody p{margin-bottom:1.28em}
  .articlebody h2{font-size:26px!important}
  .articlebody h3{font-size:21px!important}
  .articlebody blockquote{font-size:20px!important}
}
@media(max-width:430px){
  .articlepage{padding-inline:16px!important}
  .articlehead h1{font-size:clamp(31px,9vw,40px)!important}
  .articlestandfirst{font-size:15.5px}
  .articlemeta{grid-template-columns:1fr}
  .articleactions{justify-content:flex-start}
  .articlefacts{grid-row:auto}
  .articlebody{font-size:17px!important}
}
""".strip()

STYLE_RE = re.compile(r'<style id="article-critical">.*?</style>', re.I | re.S)


def main() -> None:
    pages = 0
    for path in sorted(DIST.glob("stories/*/index.html")) + sorted(DIST.glob("thoughts/*/index.html")):
        source = path.read_text(encoding="utf-8")
        if 'class="page reading articlepage"' not in source:
            continue
        source = STYLE_RE.sub("", source)
        critical = '<style id="article-critical">\n' + ARTICLE_CSS + '\n</style>'
        source = source.replace("</head>", critical + "</head>", 1)
        path.write_text(source, encoding="utf-8")
        pages += 1
    print(f"Article polish: pages={pages}, inline_critical=1")


if __name__ == "__main__":
    main()
