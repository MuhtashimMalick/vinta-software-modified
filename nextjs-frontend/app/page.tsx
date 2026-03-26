"use client";

import { useState, useEffect } from "react";
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
  CheckCircleIcon,
  XCircleIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import { ArrowsRightLeftIcon } from "@heroicons/react/24/solid";
import { clsx } from "clsx";
import axios from "axios";

import Loader from "@/components/ui/loader";

// ─── Types ────────────────────────────────────────────────────────────────────

type LogStatus = "Success" | "Skipped" | "In Progress" | "Error";

interface ActivityLog {
  id: string;
  timestamp: string;
  actionType: string;
  actionVariant:
    | "import-from-pda-to-sql"
    | "export-from-sql-to-unleashed"
    | "import-from-unleashed-to-sql";
  status: LogStatus;
  message: string;
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function StatusBadge({ status }: { status: LogStatus }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center px-2.5 py-0.5 rounded text-xs font-semibold border",
        status === "Success" &&
          "bg-green-500/20 text-green-400 border-green-500/30",
        ["In Progress", "Skipped"].includes(status) &&
          "bg-orange-500/20 text-orange-400 border-orange-500/30",
        status === "Error" && "bg-red-500/20 text-red-400 border-red-500/30",
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
    variant === "import-from-pda-to-sql" ||
    variant === "import-from-unleashed-to-sql" ? (
      <ArrowDownTrayIcon className={iconClass} />
    ) : variant === "export-from-sql-to-unleashed" ? (
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

const LOGS_PAGE_SIZE = 5;

export default function DataSyncDashboard() {
  const [showOlder, setShowOlder] = useState(false);
  const [logs, setLogs] = useState<ActivityLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [logsLoading, setLogsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<{
    message: string;
    type: "success" | "error";
  } | null>(null);
  const [expandedLogs, setExpandedLogs] = useState<Set<string>>(new Set());
  const [loadingActions, setLoadingActions] = useState<Set<string>>(new Set());

  const setActionLoading = (action: string, value: boolean) => {
    setLoadingActions((prev) => {
      const next = new Set(prev);
      value ? next.add(action) : next.delete(action);
      return next;
    });
  };

  const toggleLog = (id: string) => {
    setExpandedLogs((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const showToast = (message: string, type: "success" | "error") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 40000);
  };

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await fetch("/api/logs");
        console.log(res);
        if (!res.ok) throw new Error("Failed to fetch logs");
        const data = await res.json();
        setLogs(data);
      } catch (err) {
        setError("Could not load activity logs.");
        console.error(err);
      } finally {
        setLogsLoading(false);
      }
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 2000);
    return () => clearInterval(interval);
  }, []);

  const visibleLogs = showOlder ? logs : logs.slice(0, LOGS_PAGE_SIZE);
  const hasMoreLogs = logs.length > LOGS_PAGE_SIZE;

  async function importFromPDAToSQL() {
    setActionLoading("import-from-pda-to-sql", true);
    // const newLog: ActivityLog = {
    //   id: crypto.randomUUID(),
    //   timestamp: new Date().toISOString(),
    //   actionType: "Import from PDA to SQL",
    //   actionVariant: "import-from-pda-to-sql",
    //   status: "In Progress",
    //   message: "Importing XML files from PDA into SQL...",
    // };
    // setLogs((prev) => [newLog, ...prev]);

    try {
      const response = await axios.post(
        "http://localhost:8000/sales/import-remote-xml",
        null,
        { headers: { accept: "application/json" } },
      );

      const { imported, skipped, failed } = response.data;

      const parts = [];
      if (imported.length > 0) parts.push(`${imported.length} imported`);
      if (skipped.length > 0) parts.push(`${skipped.length} skipped`);
      if (failed.length > 0) parts.push(`${failed.length} failed`);

      const summary =
        parts.length > 0
          ? parts.join(", ")
          : "No XML files found in directory.";
      const hasFailures = failed.length > 0;

      // setLogs((prev) =>
      //   prev.map((l) =>
      //     l.id === newLog.id
      //       ? {
      //           ...l,
      //           status: hasFailures ? "Error" : "Success",
      //           message: `${summary}.`,
      //         }
      //       : l,
      //   ),
      // );

      showToast(
        hasFailures
          ? `Import finished with errors — ${summary}.`
          : `Import complete — ${summary}.`,
        hasFailures ? "error" : "success",
      );
    } catch {
      // setLogs((prev) =>
      //   prev.map((l) =>
      //     l.id === newLog.id
      //       ? {
      //           ...l,
      //           status: "Error",
      //           message: "Import failed: Could not reach the import endpoint.",
      //         }
      //       : l,
      //   ),
      // );
      showToast("Import failed. Could not reach the server.", "error");
    }
    setActionLoading("import-from-pda-to-sql", false);
  }

  async function exportFromSQLToUnleashed() {
    setActionLoading("export-from-sql-to-unleashed", true);
    // const newLog: ActivityLog = {
    //   id: crypto.randomUUID(),
    //   timestamp: new Date().toISOString(),
    //   actionType: "Export from SQL to Unleashed",
    //   actionVariant: "export-from-sql-to-unleashed",
    //   status: "In Progress",
    //   message: "Exporting sales orders from SQL to Unleashed...",
    // };
    // setLogs((prev) => [newLog, ...prev]);

    try {
      await axios.post(
        "http://localhost:8000/sales/export-sales-orders",
        null,
        {
          headers: { accept: "application/json" },
        },
      );

      // setLogs((prev) =>
      //   prev.map((l) =>
      //     l.id === newLog.id
      //       ? {
      //           ...l,
      //           status: "Success",
      //           message: "Sales orders successfully exported to Unleashed.",
      //         }
      //       : l,
      //   ),
      // );
      showToast("Sales orders exported to Unleashed successfully.", "success");
    } catch {
      // setLogs((prev) =>
      //   prev.map((l) =>
      //     l.id === newLog.id
      //       ? {
      //           ...l,
      //           status: "Error",
      //           message:
      //             "Export failed: Could not reach the sales orders endpoint.",
      //         }
      //       : l,
      //   ),
      // );
      showToast("Export failed. Could not reach the server.", "error");
    }
    setActionLoading("export-from-sql-to-unleashed", false);
  }

  async function importFromUnleashedToSQL() {
    setLoading(true);
    setActionLoading("import-from-unleashed-to-sql", true);
    // const newLog: ActivityLog = {
    //   id: crypto.randomUUID(),
    //   timestamp: new Date().toISOString(),
    //   actionType: "Import from Unleashed to SQL",
    //   actionVariant: "import-from-unleashed-to-sql",
    //   status: "In Progress",
    //   message: "Importing customers and products from Unleashed...",
    // };
    // setLogs((prev) => [newLog, ...prev]);

    try {
      // await axios.post(
      //   "http://localhost:8000/customers/import-customers-from-unleashed",
      //   null,
      //   { headers: { accept: "application/json" } },
      // );

      await axios.post("http://localhost:8000/products/import-products", null, {
        headers: { accept: "application/json" },
      });

      // setLogs((prev) =>
      //   prev.map((l) =>
      //     l.id === newLog.id
      //       ? {
      //           ...l,
      //           status: "Success",
      //           message:
      //             "Customers and products successfully imported from Unleashed.",
      //         }
      //       : l,
      //   ),
      // );
      showToast("Customers and products imported successfully.", "success");
    } catch {
      // setLogs((prev) =>
      //   prev.map((l) =>
      //     l.id === newLog.id
      //       ? {
      //           ...l,
      //           status: "Error",
      //           message:
      //             "Import failed: Could not reach one or more Unleashed endpoints.",
      //         }
      //       : l,
      //   ),
      // );
      showToast("Import failed. Could not reach the server.", "error");
    } finally {
      setLoading(false);
      setActionLoading("import-from-unleashed-to-sql", false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-[#0d1117] text-white text-sm">
      {/* ── Navbar ─────────────────────────────────────────────────────────── */}
      <header className="flex items-center justify-between px-6 py-3 bg-[#161b27] border-b border-white/[0.08] sticky top-0 z-10">
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-md bg-blue-500 flex items-center justify-center shrink-0">
            <ArrowsRightLeftIcon className="w-4 h-4 text-white" />
          </div>
          <span className="font-semibold text-[15px] tracking-tight">
            Data Sync Dashboard
          </span>
        </div>
      </header>

      {/* ── Main ───────────────────────────────────────────────────────────── */}
      <main className="flex-1 w-full max-w-6xl mx-auto px-6 py-10">
        {/* Page heading */}
        <div className="mb-8">
          {/* <h1 className="text-[2rem] font-extrabold tracking-tight leading-tight">
            Data Integration Overview
          </h1>
          <p className="text-gray-400 mt-1">
            Manage data synchronization between PDA systems and Unleashed ERP
            via SQL Server.
          </p> */}
        </div>

        {/* ── Sync Cards ──────────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
          {/* PDA → Unleashed */}
          <div className="bg-[#1a2030] rounded-xl p-5 border border-white/[0.06]">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-blue-500/20 flex items-center justify-center">
                  <svg
                    className="w-5 h-5 text-blue-400"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M5 3a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2H5zm0 2h2v2H5V5zm0 4h2v2H5V9zm0 4h2v2H5v-2zm4-8h2v2H9V5zm0 4h2v2H9V9zm0 4h2v2H9v-2zm4-8h2v2h-2V5zm0 4h2v2h-2V9zm0 4h2v2h-2v-2z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <span className="font-semibold text-[15px]">
                  PDA to Unleashed
                </span>
              </div>
              <ArrowRightIcon className="w-4 h-4 text-gray-500" />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => importFromPDAToSQL()}
                disabled={loadingActions.has("import-from-pda-to-sql")}
                className={`rounded-xl py-9 flex flex-col items-center gap-2 font-semibold transition-all
                  ${
                    loadingActions.has("import-from-pda-to-sql")
                      ? "bg-gray-600 text-gray-300 cursor-not-allowed opacity-60"
                      : "bg-blue-500 text-white hover:bg-blue-600 active:scale-[0.97] cursor-pointer"
                  }`}
              >
                <ArrowDownTrayIcon className="w-7 h-7" />
                <span className="text-sm">Import from PDA to SQL</span>
              </button>

              <button
                onClick={() => exportFromSQLToUnleashed()}
                disabled={loadingActions.has("export-from-sql-to-unleashed")}
                className={`border rounded-xl py-9 flex flex-col items-center gap-2 font-semibold transition-all
                  ${
                    loadingActions.has("export-from-sql-to-unleashed")
                      ? "border-gray-500/30 text-gray-500 cursor-not-allowed opacity-50"
                      : "border-blue-400/50 text-blue-400 hover:bg-blue-400/10 active:scale-[0.97] cursor-pointer"
                  }`}
              >
                <ArrowUpTrayIcon className="w-7 h-7" />
                <span className="text-sm">Export from SQL to Unleashed</span>
              </button>
            </div>
          </div>

          {/* Unleashed → PDA */}
          <div className="bg-[#1a2030] rounded-xl p-5 border border-white/[0.06]">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-blue-500/20 flex items-center justify-center">
                  <svg
                    className="w-5 h-5 text-blue-400"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
                    <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
                    <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
                  </svg>
                </div>
                <span className="font-semibold text-[15px]">
                  Unleashed to PDA
                </span>
              </div>
              <ArrowLeftIcon className="w-4 h-4 text-gray-500" />
            </div>

            <div className="flex justify-center">
              <div className="relative w-[calc(50%-6px)] rounded-xl">
                {loading && <Loader text="" />}

                <button
                  onClick={() => importFromUnleashedToSQL()}
                  disabled={loadingActions.has("import-from-unleashed-to-sql")}
                  className={`w-full rounded-xl py-9 flex flex-col items-center gap-2 font-semibold transition-all
                    ${
                      loadingActions.has("import-from-unleashed-to-sql")
                        ? "bg-gray-600 text-gray-300 cursor-not-allowed opacity-60"
                        : "bg-blue-500 text-white hover:bg-blue-600 active:scale-[0.97] cursor-pointer"
                    }`}
                >
                  <CloudArrowDownIcon className="w-7 h-7" />
                  <span className="text-sm">Import from Unleashed to SQL</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* ── Activity Logs ────────────────────────────────────────────────── */}
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-bold">Activity Logs</h2>
          {/* <button
            onClick={() => console.log("View Full Report")}
            className="text-blue-400 hover:text-blue-300 font-medium transition-colors text-sm"
          >
            View Full Report
          </button> */}
        </div>

        <div className="relative bg-[#1a2030] rounded-xl border border-white/[0.06] overflow-hidden">
          {logsLoading && <Loader text="Loading logs..." />}
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
              {loading ? (
                <tr>
                  <td
                    colSpan={4}
                    className="px-5 py-12 text-center text-gray-400 text-sm"
                  >
                    Loading activity logs...
                  </td>
                </tr>
              ) : error ? (
                <tr>
                  <td
                    colSpan={4}
                    className="px-5 py-12 text-center text-red-400 text-sm"
                  >
                    {error}
                  </td>
                </tr>
              ) : visibleLogs.length === 0 ? (
                <tr>
                  <td
                    colSpan={4}
                    className="px-5 py-12 text-center text-gray-500 text-sm"
                  >
                    No activity logs for today.
                  </td>
                </tr>
              ) : (
                visibleLogs.map((log, idx) => (
                  <tr
                    key={log.id}
                    className={clsx(
                      "hover:bg-white/[0.025] transition-colors",
                      idx < visibleLogs.length - 1 &&
                        "border-b border-white/[0.06]",
                    )}
                  >
                    <td className="px-5 py-4 font-mono text-xs text-gray-400 whitespace-nowrap">
                      {new Date(log.timestamp).toLocaleString(undefined, {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <ActionCell
                        variant={log.actionVariant}
                        label={log.actionType}
                      />
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <StatusBadge status={log.status} />
                    </td>
                    <td className="px-5 py-4 text-gray-300">
                      {log.message.length > 100 && !expandedLogs.has(log.id) ? (
                        <>
                          {log.message.slice(0, 100)}...{" "}
                          <button
                            onClick={() => toggleLog(log.id)}
                            className="text-blue-400 hover:text-blue-300 transition-colors"
                          >
                            See more
                          </button>
                        </>
                      ) : log.message.length > 100 ? (
                        <>
                          {log.message}{" "}
                          <button
                            onClick={() => toggleLog(log.id)}
                            className="text-blue-400 hover:text-blue-300 transition-colors"
                          >
                            Show less
                          </button>
                        </>
                      ) : (
                        log.message
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>

          {/* Load older */}
          {hasMoreLogs && (
            <div className="border-t border-white/[0.06] py-3 flex justify-center">
              <button
                onClick={() => setShowOlder((prev) => !prev)}
                className="flex items-center gap-1.5 text-gray-400 hover:text-gray-200 transition-colors text-sm cursor-pointer"
              >
                <ChevronDownIcon
                  className={clsx(
                    "w-4 h-4 transition-transform",
                    showOlder && "rotate-180",
                  )}
                />
                {showOlder
                  ? "Hide older logs"
                  : `Load older logs (${logs.length - LOGS_PAGE_SIZE} more)`}
              </button>
            </div>
          )}
        </div>
      </main>

      {/* ── Footer ─────────────────────────────────────────────────────────── */}
      <footer className="text-center py-5 text-xs text-gray-500 border-t border-white/[0.06]">
        {/* © 2023 Data Sync Engine v2.4.0 • Enterprise Edition • Connected to{" "} */}
        {/* <span className="text-blue-400 font-medium">SQL_PROD_CLUSTER</span> */}
      </footer>
      {toast && (
        <div
          className={clsx(
            "fixed bottom-6 right-6 z-50 flex items-start gap-3 px-4 py-3 rounded-xl border shadow-2xl text-sm font-medium transition-all",
            toast.type === "success"
              ? "bg-[#1a2030] border-green-500/40 text-green-400"
              : "bg-[#1a2030] border-red-500/40 text-red-400",
          )}
        >
          {toast.type === "success" ? (
            <CheckCircleIcon className="w-5 h-5 shrink-0 mt-0.5" />
          ) : (
            <XCircleIcon className="w-5 h-5 shrink-0 mt-0.5" />
          )}
          <span>{toast.message}</span>
          <button
            onClick={() => setToast(null)}
            className="ml-2 opacity-50 hover:opacity-100 transition-opacity"
          >
            <XMarkIcon className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}
