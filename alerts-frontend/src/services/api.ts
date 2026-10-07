/**
 * API service layer for communicating with the Django backend.
 */

import { Alert, PaginatedResponse } from "../types";

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL ?? "http://localhost:8000";
export const CONFIGURED_API_TOKEN = process.env.REACT_APP_API_TOKEN ?? "";

function authenticatedHeaders(token: string): HeadersInit {
  return token ? { Authorization: `Token ${token}` } : {};
}

export interface FetchAlertsParams {
  token: string;
  scope: "direct" | "subtree";
  severity?: string;
  status?: string;
  search?: string;
  pageUrl?: string | null;
}

/**
 * Fetch paginated alerts from the API.
 */
export async function fetchAlerts(
  params: FetchAlertsParams,
  signal?: AbortSignal
): Promise<PaginatedResponse<Alert>> {
  let url: string;

  if (params.pageUrl) {
    url = params.pageUrl;
  } else {
    const searchParams = new URLSearchParams();
    searchParams.set("scope", params.scope);

    if (params.severity && params.severity !== "all") {
      searchParams.set("severity", params.severity);
    }
    if (params.status && params.status !== "all") {
      searchParams.set("status", params.status);
    }
    if (params.search?.trim()) {
      searchParams.set("q", params.search.trim());
    }

    url = `${API_BASE_URL}/api/alerts?${searchParams.toString()}`;
  }

  const response = await fetch(url, {
    signal,
    headers: authenticatedHeaders(params.token),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    const errorMessage =
      errorData?.detail ?? response.statusText ?? "Failed to fetch alerts";
    throw new Error(errorMessage);
  }

  return response.json();
}

/**
 * Dismiss an alert by ID.
 */
export async function dismissAlert(alertId: string, token: string): Promise<Alert> {
  const response = await fetch(
    `${API_BASE_URL}/api/alerts/${encodeURIComponent(alertId)}/dismiss`,
    {
      method: "POST",
      headers: authenticatedHeaders(token),
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    const errorMessage =
      errorData?.detail ?? response.statusText ?? "Failed to dismiss alert";
    throw new Error(errorMessage);
  }

  return response.json();
}
