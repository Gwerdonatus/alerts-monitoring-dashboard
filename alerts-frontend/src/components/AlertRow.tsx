import React from "react";
import { Alert } from "../types";

type AlertRowProps = {
  alert: Alert;
  isStriped?: boolean;
  onDismiss?: () => void;
  isDismissing?: boolean;
};

const severityStyles: Record<string, { bg: string; text: string; border: string }> = {
  low: {
    bg: "bg-emerald-500/10",
    text: "text-emerald-300",
    border: "border-emerald-500/30",
  },
  medium: {
    bg: "bg-amber-500/10",
    text: "text-amber-300",
    border: "border-amber-500/30",
  },
  high: {
    bg: "bg-rose-500/10",
    text: "text-rose-300",
    border: "border-rose-500/30",
  },
};

const statusStyles: Record<string, { bg: string; text: string; border: string }> = {
  open: {
    bg: "bg-emerald-500/10",
    text: "text-emerald-300",
    border: "border-emerald-500/30",
  },
  dismissed: {
    bg: "bg-slate-700/30",
    text: "text-slate-400",
    border: "border-slate-600/40",
  },
};

export const AlertRow: React.FC<AlertRowProps> = ({
  alert,
  isStriped,
  onDismiss,
  isDismissing,
}) => {
  const severityStyle = severityStyles[alert.severity] ?? {
    bg: "bg-slate-800/50",
    text: "text-slate-300",
    border: "border-slate-700/50",
  };
  const statusStyle = statusStyles[alert.status] ?? {
    bg: "bg-slate-800/50",
    text: "text-slate-300",
    border: "border-slate-700/50",
  };

  const createdAt = new Date(alert.created_at);

  return (
    <tr
      className={`text-sm transition ${
        isStriped ? "bg-slate-900/60" : "bg-slate-950/60"
      } hover:bg-slate-800/80`}
    >
      <td className="whitespace-nowrap px-4 py-3">
        <div className="flex flex-col">
          <span className="font-medium text-slate-100">
            {alert.employee?.name ?? "—"}
          </span>
          <span className="text-xs text-slate-500">
            ID: {alert.employee?.id ?? "n/a"}
          </span>
        </div>
      </td>
      <td className="whitespace-nowrap px-4 py-3">
        <span
          className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-xs font-semibold capitalize ${severityStyle.bg} ${severityStyle.text} ${severityStyle.border}`}
          aria-label={`Severity: ${alert.severity}`}
        >
          <span
            className={`h-1.5 w-1.5 rounded-full ${severityStyle.bg.replace("/10", "")} ${severityStyle.border.replace("/30", "")}`}
            aria-hidden="true"
          />
          {alert.severity}
        </span>
      </td>
      <td className="max-w-xs px-4 py-3">
        <span className="line-clamp-2 text-sm font-medium text-slate-100">
          {alert.category}
        </span>
      </td>
      <td className="whitespace-nowrap px-4 py-3">
        <span
          className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-xs font-semibold capitalize ${statusStyle.bg} ${statusStyle.text} ${statusStyle.border}`}
          aria-label={`Status: ${alert.status}`}
        >
          <span
            className={`h-1.5 w-1.5 rounded-full ${statusStyle.bg.replace("/10", "").replace("/30", "")} ${statusStyle.border.replace("/30", "").replace("/40", "")}`}
            aria-hidden="true"
          />
          {alert.status}
        </span>
      </td>
      <td className="whitespace-nowrap px-4 py-3 text-xs text-slate-400">
        <time dateTime={alert.created_at}>
          {Number.isNaN(createdAt.getTime())
            ? "—"
            : createdAt.toLocaleString(undefined, {
                year: "numeric",
                month: "short",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
              })}
        </time>
      </td>
      <td className="whitespace-nowrap px-4 py-3 text-right">
        {onDismiss && (
          <button
            type="button"
            onClick={onDismiss}
            disabled={isDismissing}
            aria-label={`Dismiss alert ${alert.id}`}
            className="inline-flex items-center gap-1.5 rounded-md border border-emerald-500/50 bg-emerald-600/20 px-3 py-1.5 text-xs font-medium text-emerald-200 shadow-sm transition hover:border-emerald-400/70 hover:bg-emerald-600/30 hover:text-emerald-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:ring-offset-2 focus:ring-offset-slate-950 disabled:cursor-not-allowed disabled:border-emerald-900/30 disabled:bg-emerald-950/30 disabled:text-emerald-500/50 disabled:opacity-50"
          >
            {isDismissing ? (
              <>
                <span
                  className="h-3 w-3 animate-spin rounded-full border-2 border-emerald-300 border-t-transparent"
                  aria-hidden="true"
                />
                Dismissing…
              </>
            ) : (
              "Dismiss"
            )}
          </button>
        )}
      </td>
    </tr>
  );
};


