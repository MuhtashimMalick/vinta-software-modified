// app/api/logs/route.ts
import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const JSONL_LOGS_DIR = "C:\\Users\\FATTANI COMPUTERS\\Documents\\segwayz\\nextjs-fastapi-template\\fastapi_backend\\logs\\jsonl"; // same path as in logging_config.py

export async function GET() {
  try {
    const today = new Date();
    const day = String(today.getUTCDate()).padStart(2, "0");
    const month = String(today.getUTCMonth() + 1).padStart(2, "0");
    const year = today.getUTCFullYear();
    const filename = `${day}-${month}-${year}.log`;
    const filepath = path.join(JSONL_LOGS_DIR, filename);

    if (!fs.existsSync(filepath)) {
      return NextResponse.json([]);
    }

    const content = fs.readFileSync(filepath, "utf-8");

    const logs = content
      .split("\n")
      .filter((line) => line.trim() !== "")
      .map((line) => JSON.parse(line))
      .reverse(); // most recent first

    return NextResponse.json(logs);
  } catch (error) {
    console.error("Failed to read logs file:", error);
    return NextResponse.json({ error: "Failed to load logs" }, { status: 500 });
  }
}
