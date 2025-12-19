/**
 * Type definitions for the Alerts Dashboard application.
 */

export type AlertSeverity = "low" | "medium" | "high";
export type AlertStatus = "open" | "dismissed";
export type ScopeOption = "direct" | "subtree";

export interface Employee {
  id: string;
  name: string;
}

export interface Alert {
  id: string;
  employee: Employee;
  severity: AlertSeverity;
  category: string;
  created_at: string;
  status: AlertStatus;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface FilterState {
  severity: "all" | AlertSeverity;
  status: "all" | AlertStatus;
  scope: ScopeOption;
  search: string;
}


