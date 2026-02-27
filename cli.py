# cli.py — Phase 9: CLI entry point
# doorway serve  → start API server
# doorway run    → run single input

import argparse
import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Doorway AGI")
    sub = parser.add_subparsers(dest="command")
    serve = sub.add_parser("serve", help="Start API server")
    serve.add_argument("--host", default="0.0.0.0")
    serve.add_argument("--port", type=int, default=8000)
    rp = sub.add_parser("run", help="Run single input")
    rp.add_argument("input", type=str)
    args = parser.parse_args()
    if args.command == "serve":
        uvicorn.run("api.server:app", host=args.host, port=args.port)
    elif args.command == "run":
        from main import run
        run(args.input)


if __name__ == "__main__":
    main()
