const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
).replace(/\/$/, '')

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Accept: 'application/json',
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...options.headers,
    },
    ...options,
  })

  const payload = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(payload.detail || `Request failed with status ${response.status}`)
  }
  return payload
}

function queryString({ startDate, endDate } = {}) {
  const params = new URLSearchParams()
  if (startDate) params.set('start_date', startDate)
  if (endDate) params.set('end_date', endDate)
  const value = params.toString()
  return value ? `?${value}` : ''
}

function post(path, body) {
  return request(path, { method: 'POST', body: JSON.stringify(body) })
}

export const api = {
  baseUrl: API_BASE_URL,

  listIndexes() {
    return request('/api/v1/indexes')
  },

  getPrices(indexName, filters) {
    return request(
      `/api/v1/indexes/${encodeURIComponent(indexName)}/prices${queryString(filters)}`,
    )
  },

  getRentability(indexName, filters) {
    return request(
      `/api/v1/indexes/${encodeURIComponent(indexName)}/rentability${queryString(filters)}`,
    )
  },

  getDrawdown(indexName, filters) {
    return request(
      `/api/v1/indexes/${encodeURIComponent(indexName)}/drawdown${queryString(filters)}`,
    )
  },

  getComparative(indexes, filters) {
    return post('/api/v1/analyses/comparative', {
      indexes,
      start_date: filters.startDate || null,
      end_date: filters.endDate || null,
    })
  },

  getRiskReturn(indexes, filters) {
    return post('/api/v1/analyses/risk-return', {
      indexes,
      start_date: filters.startDate || null,
      end_date: filters.endDate || null,
    })
  },

  getCorrelation(indexes, interval, filters) {
    return post('/api/v1/analyses/correlation', {
      indexes,
      interval,
      start_date: filters.startDate || null,
      end_date: filters.endDate || null,
    })
  },
}
