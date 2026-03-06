"use client";

import { useState } from "react";
import {
  ArrowRightIcon,
  ArrowLeftIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  CloudArrowDownIcon,
  ArrowRightCircleIcon,
  Cog6ToothIcon,
  BellIcon,
  ChevronDownIcon,
} from "@heroicons/react/24/outline";
import { ArrowsRightLeftIcon } from "@heroicons/react/24/solid";
import { clsx } from "clsx";

// ─── Types ────────────────────────────────────────────────────────────────────

type LogStatus = "Success" | "In Progress" | "Error";

interface ActivityLog {
  id: number;
  timestamp: string;
  actionType: string;
  actionVariant: "import-pda" | "export-unleashed" | "export-pda" | "import-erp";
  status: LogStatus;
  message: string;
}

// ─── Sample Data ──────────────────────────────────────────────────────────────

const SAMPLE_LOGS: ActivityLog[] = [
  {
    id: 1,
    timestamp: "2023-10-27 14:30:22",
    actionType: "Import PDA",
    actionVariant: "import-pda",
    status: "Success",
    message: "Successfully synced 154 inventory items from PDA Group A.",
  },
  {
    id: 2,
    timestamp: "2023-10-27 14:15:05",
    actionType: "Export Unleashed",
    actionVariant: "export-unleashed",
    status: "In Progress",
    message: "Processing purchase orders for Q4 replenishment...",
  },
  {
    id: 3,
    timestamp: "2023-10-27 13:45:10",
    actionType: "Export PDA",
    actionVariant: "export-pda",
    status: "Error",
    message: "Connection timeout: Could not reach SQL Server instance PDA_DB_01.",
  },
  {
    id: 4,
    timestamp: "2023-10-27 12:00:00",
    actionType: "Import ERP",
    actionVariant: "import-erp",
    status: "Success",
    message: "Master product list updated from Unleashed API.",
  },
];

const OLDER_LOGS: ActivityLog[] = [
  {
    id: 5,
    timestamp: "2023-10-27 10:30:00",
    actionType: "Import PDA",
    actionVariant: "import-pda",
    status: "Success",
    message: "Successfully synced 98 inventory items from PDA Group B.",
  },
  {
    id: 6,
    timestamp: "2023-10-27 09:00:00",
    actionType: "Export Unleashed",
    actionVariant: "export-unleashed",
    status: "Success",
    message: "Exported 212 purchase orders to Unleashed ERP.",
  },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function StatusBadge({ status }: { status: LogStatus }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center px-2.5 py-0.5 rounded text-xs font-semibold border",
        status === "Success" && "bg-green-500/20 text-green-400 border-green-500/30",
        status === "In Progress" && "bg-orange-500/20 text-orange-400 border-orange-500/30",
        status === "Error" && "bg-red-500/20 text-red-400 border-red-500/30"
      )}
    >
      {status}
    </span>
  );
}

function ActionCell({
  variant,
  label,
}: {
  variant: ActivityLog["actionVariant"];
  label: string;
}) {
  const iconClass = "w-4 h-4 shrink-0 text-blue-400";

  const icon =
    variant === "import-pda" || variant === "import-erp" ? (
      <ArrowDownTrayIcon className={iconClass} />
    ) : variant === "export-unleashed" ? (
      <ArrowUpTrayIcon className={iconClass} />
    ) : (
      <ArrowRightCircleIcon className={iconClass} />
    );

  return (
    <span className="inline-flex items-center gap-1.5 font-medium text-white">
      {icon}
      {label}
    </span>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function DataSyncDashboard() {
  const [showOlder, setShowOlder] = useState(false);

  const visibleLogs = showOlder ? [...SAMPLE_LOGS, ...OLDER_LOGS] : SAMPLE_LOGS;

  return (
    <div className="min-h-screen flex flex-col bg-[#0d1117] text-white text-sm">
      {/* ── Navbar ─────────────────────────────────────────────────────────── */}
      <header className="flex items-center justify-between px-6 py-3 bg-[#161b27] border-b border-white/[0.08] sticky top-0 z-10">
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-md bg-blue-500 flex items-center justify-center shrink-0">
            <ArrowsRightLeftIcon className="w-4 h-4 text-white" />
          </div>
          <span className="font-semibold text-[15px] tracking-tight">Data Sync Dashboard</span>
        </div>

        {/* Right actions */}
        <div className="flex items-center gap-2">
          {/* Connection badge */}
          <div className="flex items-center gap-1.5 border border-green-500/40 bg-green-500/10 text-green-400 text-xs font-bold px-3 py-1.5 rounded-md tracking-wide uppercase">
            <span className="w-2 h-2 rounded-full bg-green-400" />
            SQL Server Connected
          </div>

          <button
            onClick={() => console.log("Settings")}
            className="w-9 h-9 rounded-md bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors"
          >
            <Cog6ToothIcon className="w-5 h-5 text-gray-300" />
          </button>

          <button
            onClick={() => console.log("Notifications")}
            className="w-9 h-9 rounded-md bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors"
          >
            <BellIcon className="w-5 h-5 text-gray-300" />
          </button>

          {/* Avatar */}
          <div className="w-9 h-9 rounded-full bg-orange-400 flex items-center justify-center font-bold text-white text-sm shrink-0">
            J
          </div>
        </div>
      </header>

      {/* ── Main ───────────────────────────────────────────────────────────── */}
      <main className="flex-1 w-full max-w-6xl mx-auto px-6 py-10">
        {/* Page heading */}
        <div className="mb-8">
          <h1 className="text-[2rem] font-extrabold tracking-tight leading-tight">
            Data Integration Overview
          </h1>
          <p className="text-gray-400 mt-1">
            Manage data synchronization between PDA systems and Unleashed ERP via SQL Server.
          </p>
        </div>

        {/* ── Sync Cards ──────────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
          {/* PDA → Unleashed */}
          <div className="bg-[#1a2030] rounded-xl p-5 border border-white/[0.06]">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-blue-500/20 flex items-center justify-center">
                  {/* table/grid icon */}
                  <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M5 3a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2H5zm0 2h2v2H5V5zm0 4h2v2H5V9zm0 4h2v2H5v-2zm4-8h2v2H9V5zm0 4h2v2H9V9zm0 4h2v2H9v-2zm4-8h2v2h-2V5zm0 4h2v2h-2V9zm0 4h2v2h-2v-2z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <span className="font-semibold text-[15px]">PDA to Unleashed</span>
              </div>
              <ArrowRightIcon className="w-4 h-4 text-gray-500" />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => console.log("Import from PDA")}
                className="bg-blue-500 hover:bg-blue-600 active:scale-[0.97] transition-all rounded-xl py-9 flex flex-col items-center gap-2 font-semibold cursor-pointer"
              >
                <ArrowDownTrayIcon className="w-7 h-7" />
                <span className="text-sm">Import from PDA</span>
              </button>

              <button
                onClick={() => console.log("Export to Unleashed")}
                className="border border-blue-400/50 hover:bg-blue-400/10 active:scale-[0.97] transition-all rounded-xl py-9 flex flex-col items-center gap-2 text-blue-400 font-semibold cursor-pointer"
              >
                <ArrowUpTrayIcon className="w-7 h-7" />
                <span className="text-sm">Export to Unleashed</span>
              </button>
            </div>
          </div>

          {/* Unleashed → PDA */}
          <div className="bg-[#1a2030] rounded-xl p-5 border border-white/[0.06]">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-blue-500/20 flex items-center justify-center">
                  {/* database icon */}
                  <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
                    <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
                    <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
                  </svg>
                </div>
                <span className="font-semibold text-[15px]">Unleashed to PDA</span>
              </div>
              <ArrowLeftIcon className="w-4 h-4 text-gray-500" />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => console.log("Import from ERP")}
                className="bg-blue-500 hover:bg-blue-600 active:scale-[0.97] transition-all rounded-xl py-9 flex flex-col items-center gap-2 font-semibold cursor-pointer"
              >
                <CloudArrowDownIcon className="w-7 h-7" />
                <span className="text-sm">Import from ERP</span>
              </button>

              <button
                onClick={() => console.log("Export to PDA")}
                className="border border-blue-400/50 hover:bg-blue-400/10 active:scale-[0.97] transition-all rounded-xl py-9 flex flex-col items-center gap-2 text-blue-400 font-semibold cursor-pointer"
              >
                <ArrowRightCircleIcon className="w-7 h-7" />
                <span className="text-sm">Export to PDA</span>
              </button>
            </div>
          </div>
        </div>

        {/* ── Activity Logs ────────────────────────────────────────────────── */}
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-bold">Activity Logs</h2>
          <button
            onClick={() => console.log("View Full Report")}
            className="text-blue-400 hover:text-blue-300 font-medium transition-colors text-sm"
          >
            View Full Report
          </button>
        </div>

        <div className="bg-[#1a2030] rounded-xl border border-white/[0.06] overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/[0.06]">
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wider px-5 py-3.5 w-48">
                  Timestamp
                </th>
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wider px-5 py-3.5 w-44">
                  Action Type
                </th>
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wider px-5 py-3.5 w-36">
                  Status
                </th>
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wider px-5 py-3.5">
                  Message
                </th>
              </tr>
            </thead>
            <tbody>
              {visibleLogs.map((log, idx) => (
                <tr
                  key={log.id}
                  className={clsx(
                    "hover:bg-white/[0.025] transition-colors",
                    idx < visibleLogs.length - 1 && "border-b border-white/[0.06]"
                  )}
                >
                  <td className="px-5 py-4 font-mono text-xs text-gray-400 whitespace-nowrap">
                    {log.timestamp}
                  </td>
                  <td className="px-5 py-4 whitespace-nowrap">
                    <ActionCell variant={log.actionVariant} label={log.actionType} />
                  </td>
                  <td className="px-5 py-4 whitespace-nowrap">
                    <StatusBadge status={log.status} />
                  </td>
                  <td className="px-5 py-4 text-gray-300">{log.message}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Load older */}
          <div className="border-t border-white/[0.06] py-3 flex justify-center">
            <button
              onClick={() => {
                setShowOlder((prev) => !prev);
                console.log("Load older logs");
              }}
              className="flex items-center gap-1.5 text-gray-400 hover:text-gray-200 transition-colors text-sm cursor-pointer"
            >
              <ChevronDownIcon
                className={clsx(
                  "w-4 h-4 transition-transform",
                  showOlder && "rotate-180"
                )}
              />
              {showOlder ? "Hide older logs" : "Load older logs"}
            </button>
          </div>
        </div>
      </main>

      {/* ── Footer ─────────────────────────────────────────────────────────── */}
      <footer className="text-center py-5 text-xs text-gray-500 border-t border-white/[0.06]">
        © 2023 Data Sync Engine v2.4.0 • Enterprise Edition • Connected to{" "}
        <span className="text-blue-400 font-medium">SQL_PROD_CLUSTER</span>
      </footer>
    </div>
  );
}