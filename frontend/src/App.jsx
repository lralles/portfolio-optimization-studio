import { useEffect, useMemo, useState } from 'react'
import { api } from './api'

const COLORS = ['#56d8be', '#f4b75e', '#8d9eff', '#ef7b9a', '#72b8ff', '#c39af5']

const NAV_ITEMS = [
  { id: 'overview', label: 'Overview', icon: '◒' },
  { id: 'compare', label: 'Compare indexes', icon: '◫' },
  { id: 'correlation', label: 'Correlation', icon: '⌘' },
  { id: 'portfolio', label: 'Portfolio testing', icon: '◈' },
]

const DEFAULT_FILTERS = {
  startDate: '2015-01-01',
  endDate: '',
}

function formatNumber(value, digits = 2) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '—'
  return number.toLocaleString('en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })
}

function formatPercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '—'
  return `${number >= 0 ? '+' : ''}${formatNumber(number)}%`
}

function formatDate(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
}

function downsample(rows = [], valueKey, limit = 160) {
  const valid = rows.filter((row) => Number.isFinite(Number(row[valueKey])))
  if (valid.length <= limit) return valid
  return Array.from({ length: limit }, (_, index) => {
    const sourceIndex = Math.round((index * (valid.length - 1)) / (limit - 1))
    return valid[sourceIndex]
  })
}

function ErrorBanner({ message }) {
  if (!message) return null
  return (
    <div className="error-banner" role="alert">
      <span className="error-icon">!</span>
      <span>{message}</span>
    </div>
  )
}

function LoadingState({ label = 'Loading analysis' }) {
  return (
    <div className="loading-state">
      <span className="spinner" />
      <span>{label}</span>
    </div>
  )
}

function EmptyState({ title, detail }) {
  return (
    <div className="empty-state">
      <div className="empty-mark">∿</div>
      <strong>{title}</strong>
      {detail && <span>{detail}</span>}
    </div>
  )
}

function MetricCard({ label, value, detail, accent = 'mint' }) {
  return (
    <article className={`metric-card metric-${accent}`}>
      <span className="metric-label">{label}</span>
      <strong className="metric-value">{value}</strong>
      {detail && <span className="metric-detail">{detail}</span>}
    </article>
  )
}

function Panel({ title, eyebrow, action, children, className = '' }) {
  return (
    <section className={`panel ${className}`}>
      <div className="panel-heading">
        <div>
          {eyebrow && <span className="eyebrow">{eyebrow}</span>}
          <h2>{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </section>
  )
}

function LineChart({ rows, valueKey, color = '#56d8be', suffix = '%' }) {
  const data = useMemo(() => downsample(rows, valueKey), [rows, valueKey])
  if (!data.length) {
    return <EmptyState title="No observations for this period" />
  }

  const width = 760
  const height = 270
  const padding = { top: 24, right: 22, bottom: 34, left: 52 }
  const values = data.map((row) => Number(row[valueKey]))
  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1
  const x = (index) => padding.left + (index * (width - padding.left - padding.right)) / Math.max(data.length - 1, 1)
  const y = (value) => padding.top + ((max - value) * (height - padding.top - padding.bottom)) / range
  const path = data.map((row, index) => `${index === 0 ? 'M' : 'L'} ${x(index)} ${y(Number(row[valueKey]))}`).join(' ')
  const area = `${path} L ${x(data.length - 1)} ${height - padding.bottom} L ${x(0)} ${height - padding.bottom} Z`
  const ticks = [max, min + range / 2, min]

  return (
    <div className="chart-wrap">
      <svg className="line-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Performance chart">
        <defs>
          <linearGradient id={`area-${valueKey}`} x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity=".24" />
            <stop offset="100%" stopColor={color} stopOpacity="0" />
          </linearGradient>
        </defs>
        {ticks.map((tick, index) => (
          <g key={index}>
            <line x1={padding.left} x2={width - padding.right} y1={y(tick)} y2={y(tick)} className="chart-grid" />
            <text x={padding.left - 10} y={y(tick) + 4} textAnchor="end" className="chart-label">
              {formatNumber(tick)}{suffix}
            </text>
          </g>
        ))}
        <path d={area} fill={`url(#area-${valueKey})`} />
        <path d={path} fill="none" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
        <text x={padding.left} y={height - 9} className="chart-label">{formatDate(data[0].date)}</text>
        <text x={width - padding.right} y={height - 9} textAnchor="end" className="chart-label">{formatDate(data[data.length - 1].date)}</text>
      </svg>
    </div>
  )
}

function MultiLineChart({ series }) {
  const prepared = series
    .map((item) => ({ ...item, data: downsample(item.data, 'rentability') }))
    .filter((item) => item.data.length)
  if (!prepared.length) return <EmptyState title="No comparison data" />

  const width = 760
  const height = 300
  const padding = { top: 24, right: 22, bottom: 34, left: 52 }
  const values = prepared.flatMap((item) => item.data.map((row) => Number(row.rentability)))
  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1
  const longest = Math.max(...prepared.map((item) => item.data.length))
  const x = (index) => padding.left + (index * (width - padding.left - padding.right)) / Math.max(longest - 1, 1)
  const y = (value) => padding.top + ((max - value) * (height - padding.top - padding.bottom)) / range
  const ticks = [max, min + range / 2, min]

  return (
    <div className="chart-wrap">
      <svg className="line-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Index comparison chart">
        {ticks.map((tick, index) => (
          <g key={index}>
            <line x1={padding.left} x2={width - padding.right} y1={y(tick)} y2={y(tick)} className="chart-grid" />
            <text x={padding.left - 10} y={y(tick) + 4} textAnchor="end" className="chart-label">{formatNumber(tick)}%</text>
          </g>
        ))}
        {prepared.map((item, seriesIndex) => {
          const path = item.data.map((row, index) => `${index === 0 ? 'M' : 'L'} ${x(index)} ${y(Number(row.rentability))}`).join(' ')
          return <path key={item.name} d={path} fill="none" stroke={COLORS[seriesIndex % COLORS.length]} strokeWidth="2.5" strokeLinecap="round" />
        })}
      </svg>
      <div className="legend">
        {prepared.map((item, index) => (
          <span className="legend-item" key={item.name}>
            <i style={{ backgroundColor: COLORS[index % COLORS.length] }} />
            {item.name}
          </span>
        ))}
      </div>
    </div>
  )
}

function ScatterPlot({ rows }) {
  const data = rows.filter((row) => Number.isFinite(Number(row.annualized_return)) && Number.isFinite(Number(row.annualized_volatility)))
  if (!data.length) return <EmptyState title="No risk-return observations" />

  const width = 760
  const height = 310
  const padding = { top: 22, right: 24, bottom: 44, left: 60 }
  const xValues = data.map((row) => Number(row.annualized_volatility))
  const yValues = data.map((row) => Number(row.annualized_return))
  const minX = Math.min(...xValues)
  const maxX = Math.max(...xValues)
  const minY = Math.min(...yValues)
  const maxY = Math.max(...yValues)
  const xRange = maxX - minX || 1
  const yRange = maxY - minY || 1
  const x = (value) => padding.left + ((value - minX) * (width - padding.left - padding.right)) / xRange
  const y = (value) => height - padding.bottom - ((value - minY) * (height - padding.top - padding.bottom)) / yRange

  return (
    <div className="chart-wrap">
      <svg className="scatter-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Risk return scatter plot">
        {[0, 0.5, 1].map((step) => (
          <g key={step}>
            <line x1={padding.left} x2={width - padding.right} y1={padding.top + step * (height - padding.top - padding.bottom)} y2={padding.top + step * (height - padding.top - padding.bottom)} className="chart-grid" />
            <line x1={padding.left + step * (width - padding.left - padding.right)} x2={padding.left + step * (width - padding.left - padding.right)} y1={padding.top} y2={height - padding.bottom} className="chart-grid vertical" />
          </g>
        ))}
        {data.map((row, index) => (
          <g key={row.index}>
            <circle cx={x(Number(row.annualized_volatility))} cy={y(Number(row.annualized_return))} r="7" fill={COLORS[index % COLORS.length]} className="scatter-point" />
            <text x={x(Number(row.annualized_volatility)) + 10} y={y(Number(row.annualized_return)) + 4} className="scatter-label">{row.index}</text>
          </g>
        ))}
        <text x={width / 2} y={height - 9} textAnchor="middle" className="axis-label">Annualized volatility</text>
        <text x="14" y={height / 2} transform={`rotate(-90 14 ${height / 2})`} textAnchor="middle" className="axis-label">Annualized return</text>
      </svg>
    </div>
  )
}

function IndexPicker({ indexes, selected, onChange }) {
  const toggle = (name) => {
    if (selected.includes(name)) {
      if (selected.length > 1) onChange(selected.filter((item) => item !== name))
      return
    }
    onChange([...selected, name])
  }

  return (
    <div className="index-picker">
      {indexes.map((name) => (
        <label className={`index-option ${selected.includes(name) ? 'selected' : ''}`} key={name}>
          <input type="checkbox" checked={selected.includes(name)} onChange={() => toggle(name)} />
          <span>{name}</span>
        </label>
      ))}
    </div>
  )
}

function CorrelationTable({ rows }) {
  if (!rows?.length) return <EmptyState title="No correlation observations" />
  const columns = Object.keys(rows[0]).filter((key) => key !== 'index')
  const background = (value) => {
    const number = Number(value)
    if (!Number.isFinite(number)) return 'transparent'
    const hue = number >= 0 ? 163 : 345
    const opacity = Math.min(Math.abs(number) * 0.7 + 0.08, 0.78)
    return `hsla(${hue}, 68%, 62%, ${opacity})`
  }

  return (
    <div className="table-scroll">
      <table className="correlation-table">
        <thead>
          <tr><th>Index</th>{columns.map((column) => <th key={column}>{column}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.index}>
              <th>{row.index}</th>
              {columns.map((column) => <td style={{ background: background(row[column]) }} key={column}>{formatNumber(row[column], 3)}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function App() {
  const [indexes, setIndexes] = useState([])
  const [selectedIndex, setSelectedIndex] = useState('bovespa')
  const [selectedComparison, setSelectedComparison] = useState(['bovespa', 'ifix', 'sp500brl'])
  const [filters, setFilters] = useState(DEFAULT_FILTERS)
  const [draftFilters, setDraftFilters] = useState(DEFAULT_FILTERS)
  const [activeView, setActiveView] = useState('overview')
  const [overview, setOverview] = useState(null)
  const [comparison, setComparison] = useState(null)
  const [correlation, setCorrelation] = useState(null)
  const [correlationInterval, setCorrelationInterval] = useState('month')
  const [loading, setLoading] = useState({ indexes: true, overview: false, comparison: false, correlation: false })
  const [error, setError] = useState({ indexes: '', overview: '', comparison: '', correlation: '' })

  useEffect(() => {
    let active = true
    api.listIndexes()
      .then((payload) => {
        if (!active) return
        const names = payload.indexes || []
        setIndexes(names)
        if (names.length && !names.includes(selectedIndex)) setSelectedIndex(names[0])
        setSelectedComparison((current) => {
          const valid = current.filter((name) => names.includes(name))
          return valid.length >= 2 ? valid : names.filter((name) => ['bovespa', 'ifix', 'sp500brl'].includes(name)).slice(0, 3)
        })
        setLoading((current) => ({ ...current, indexes: false }))
      })
      .catch((reason) => {
        if (!active) return
        setError((current) => ({ ...current, indexes: reason.message }))
        setLoading((current) => ({ ...current, indexes: false }))
      })
    return () => { active = false }
  }, [])

  useEffect(() => {
    if (!selectedIndex) return undefined
    let active = true
    setLoading((current) => ({ ...current, overview: true }))
    setError((current) => ({ ...current, overview: '' }))
    Promise.all([
      api.getPrices(selectedIndex, filters),
      api.getRentability(selectedIndex, filters),
      api.getDrawdown(selectedIndex, filters),
    ])
      .then(([prices, rentability, drawdown]) => {
        if (active) setOverview({ prices, rentability, drawdown })
      })
      .catch((reason) => {
        if (active) setError((current) => ({ ...current, overview: reason.message }))
      })
      .finally(() => {
        if (active) setLoading((current) => ({ ...current, overview: false }))
      })
    return () => { active = false }
  }, [selectedIndex, filters])

  useEffect(() => {
    if (activeView !== 'compare' || selectedComparison.length < 2) return undefined
    let active = true
    setLoading((current) => ({ ...current, comparison: true }))
    setError((current) => ({ ...current, comparison: '' }))
    Promise.all([
      api.getRiskReturn(selectedComparison, filters),
      api.getComparative(selectedComparison, filters),
    ])
      .then(([riskReturn, comparative]) => {
        if (active) setComparison({ riskReturn, comparative })
      })
      .catch((reason) => {
        if (active) setError((current) => ({ ...current, comparison: reason.message }))
      })
      .finally(() => {
        if (active) setLoading((current) => ({ ...current, comparison: false }))
      })
    return () => { active = false }
  }, [activeView, selectedComparison, filters])

  useEffect(() => {
    if (activeView !== 'correlation' || selectedComparison.length < 2) return undefined
    let active = true
    setLoading((current) => ({ ...current, correlation: true }))
    setError((current) => ({ ...current, correlation: '' }))
    api.getCorrelation(selectedComparison, correlationInterval, filters)
      .then((payload) => {
        if (active) setCorrelation(payload)
      })
      .catch((reason) => {
        if (active) setError((current) => ({ ...current, correlation: reason.message }))
      })
      .finally(() => {
        if (active) setLoading((current) => ({ ...current, correlation: false }))
      })
    return () => { active = false }
  }, [activeView, selectedComparison, correlationInterval, filters])

  const applyFilters = (event) => {
    event.preventDefault()
    setFilters(draftFilters)
  }

  const currentView = NAV_ITEMS.find((item) => item.id === activeView)
  const selectedName = selectedIndex || 'No index selected'

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><span /></div>
          <div><strong>Portfolio</strong><span>Optimization Studio</span></div>
        </div>

        <div className="sidebar-section-label">Workspace</div>
        <nav className="main-nav" aria-label="Main navigation">
          {NAV_ITEMS.map((item) => (
            <button className={`nav-item ${activeView === item.id ? 'active' : ''}`} onClick={() => setActiveView(item.id)} key={item.id}>
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
              {activeView === item.id && <i />}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="data-note">
            <span className="data-note-icon">↗</span>
            <div><strong>Historical data</strong><span>Consumer-backed analysis</span></div>
          </div>
          <span className="version">API v1 · local workspace</span>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb"><span>Studio</span><b>/</b><strong>{currentView?.label}</strong></div>
          <div className="topbar-actions">
            <span className={`connection-status ${loading.indexes ? 'pending' : error.indexes ? 'offline' : ''}`}>
              <i /> {loading.indexes ? 'Connecting to API' : error.indexes ? 'API unavailable' : 'API connected'}
            </span>
            <button className="refresh-button" onClick={() => window.location.reload()} title="Reload application">↻</button>
          </div>
        </header>

        <div className="content-wrap">
          <div className="page-intro">
            <div>
              <span className="eyebrow">Market intelligence</span>
              <h1>{activeView === 'overview' ? 'Understand the shape of your market' : currentView?.label}</h1>
              <p>Explore historical performance and portfolio relationships from your cleaned index data.</p>
            </div>
            <div className="date-filter-card">
              <form onSubmit={applyFilters}>
                <label><span>From</span><input type="date" value={draftFilters.startDate} onChange={(event) => setDraftFilters({ ...draftFilters, startDate: event.target.value })} /></label>
                <label><span>To</span><input type="date" value={draftFilters.endDate} onChange={(event) => setDraftFilters({ ...draftFilters, endDate: event.target.value })} /></label>
                <button type="submit" className="apply-button">Apply range <span>→</span></button>
              </form>
            </div>
          </div>

          <ErrorBanner message={error.indexes} />
          {activeView === 'overview' && (
            <OverviewView
              indexes={indexes}
              selectedIndex={selectedIndex}
              setSelectedIndex={setSelectedIndex}
              overview={overview}
              loading={loading.overview}
              error={error.overview}
              selectedName={selectedName}
            />
          )}
          {activeView === 'compare' && (
            <CompareView
              indexes={indexes}
              selected={selectedComparison}
              setSelected={setSelectedComparison}
              comparison={comparison}
              loading={loading.comparison}
              error={error.comparison}
            />
          )}
          {activeView === 'correlation' && (
            <CorrelationView
              indexes={indexes}
              selected={selectedComparison}
              setSelected={setSelectedComparison}
              correlation={correlation}
              interval={correlationInterval}
              setInterval={setCorrelationInterval}
              loading={loading.correlation}
              error={error.correlation}
            />
          )}
          {activeView === 'portfolio' && <PortfolioTestingView indexes={indexes} filters={filters} />}
        </div>
      </main>
    </div>
  )
}

function OverviewView({ indexes, selectedIndex, setSelectedIndex, overview, loading, error, selectedName }) {
  const priceRows = overview?.prices?.data || []
  const rentability = overview?.rentability
  const drawdownRows = overview?.drawdown?.drawdown || []
  const latest = priceRows[priceRows.length - 1]
  const maxDrawdown = drawdownRows.length ? Math.min(...drawdownRows.map((row) => Number(row.drawdown)).filter(Number.isFinite)) : null

  return (
    <>
      <div className="selection-row">
        <div className="select-wrap">
          <span className="select-label">Focus index</span>
          <select value={selectedIndex} onChange={(event) => setSelectedIndex(event.target.value)} disabled={!indexes.length}>
            {indexes.map((name) => <option key={name} value={name}>{name}</option>)}
          </select>
        </div>
        <span className="selection-helper">All calculations are performed by the web API.</span>
      </div>
      <ErrorBanner message={error} />
      {loading && <LoadingState label={`Loading ${selectedName} analysis`} />}
      {!loading && overview && (
        <>
          <div className="metric-grid">
            <MetricCard label="Total return" value={formatPercent(rentability?.total_return)} detail="Across selected period" accent="mint" />
            <MetricCard label="Annualized return" value={formatPercent(rentability?.annualized_return)} detail="Compounded performance" accent="gold" />
            <MetricCard label="Annualized volatility" value={`${formatNumber(rentability?.annualized_volatility)}%`} detail="Historical risk" accent="blue" />
            <MetricCard label="Maximum drawdown" value={`${formatNumber(maxDrawdown)}%`} detail="Peak to trough" accent="pink" />
          </div>
          <div className="overview-grid">
            <Panel title="Relative performance" eyebrow={`${selectedName} · rentability`} action={<span className="panel-meta">{priceRows.length.toLocaleString()} observations</span>}>
              <LineChart rows={rentability?.rentability} valueKey="rentability" />
            </Panel>
            <Panel title="Current snapshot" eyebrow="Latest available observation" className="snapshot-panel">
              <div className="snapshot-value">{formatNumber(latest?.price)}</div>
              <span className="snapshot-label">Latest index level</span>
              <div className="snapshot-divider" />
              <div className="snapshot-row"><span>Observation date</span><strong>{latest ? formatDate(latest.date) : '—'}</strong></div>
              <div className="snapshot-row"><span>Starting level</span><strong>{formatNumber(priceRows[0]?.price)}</strong></div>
              <div className="snapshot-row"><span>Data points</span><strong>{priceRows.length.toLocaleString()}</strong></div>
            </Panel>
          </div>
          <Panel title="Drawdown profile" eyebrow="Distance from running peak" className="drawdown-panel">
            <LineChart rows={drawdownRows} valueKey="drawdown" color="#ef7b9a" />
          </Panel>
        </>
      )}
      {!loading && !overview && !error && <EmptyState title="Choose an index to begin" detail="The API response will appear here." />}
    </>
  )
}

function CompareView({ indexes, selected, setSelected, comparison, loading, error }) {
  const riskRows = comparison?.riskReturn?.results_df || []
  const timeseries = Object.entries(comparison?.comparative?.rentability_timeseries || {}).map(([name, data]) => ({ name, data }))
  return (
    <>
      <Panel title="Choose indexes to compare" eyebrow="Consumer universe" action={<span className="panel-meta">{selected.length} selected</span>}>
        <IndexPicker indexes={indexes} selected={selected} onChange={setSelected} />
      </Panel>
      <ErrorBanner message={error} />
      {loading && <LoadingState label="Comparing selected indexes" />}
      {!loading && comparison && (
        <>
          <div className="comparison-grid">
            <Panel title="Risk / return map" eyebrow="Annualized figures">
              <ScatterPlot rows={riskRows} />
            </Panel>
            <Panel title="Performance leaders" eyebrow="Across selected period" className="table-panel">
              <AnalysisTable rows={riskRows} columns={[['index', 'Index'], ['annualized_return', 'Return'], ['annualized_volatility', 'Risk']]} percentColumns={['annualized_return', 'annualized_volatility']} />
            </Panel>
          </div>
          <Panel title="Relative performance" eyebrow="Normalized to each index's first observation">
            <MultiLineChart series={timeseries} />
          </Panel>
        </>
      )}
      {!loading && !comparison && !error && <EmptyState title="Select at least two indexes" detail="Choose the series you want to compare above." />}
    </>
  )
}

function CorrelationView({ indexes, selected, setSelected, correlation, interval, setInterval, loading, error }) {
  return (
    <>
      <Panel title="Choose indexes to correlate" eyebrow="Return relationship" action={<div className="segmented-control">{['daily', 'month', 'year'].map((item) => <button className={interval === item ? 'active' : ''} onClick={() => setInterval(item)} key={item}>{item}</button>)}</div>}>
        <IndexPicker indexes={indexes} selected={selected} onChange={setSelected} />
      </Panel>
      <ErrorBanner message={error} />
      {loading && <LoadingState label={`Computing ${interval} correlations`} />}
      {!loading && correlation && (
        <div className="correlation-layout">
          <Panel title="Correlation matrix" eyebrow={`${interval} return variation`}>
            <CorrelationTable rows={correlation.correlation_matrix} />
          </Panel>
          <Panel title="Observations" eyebrow="Aligned return series" className="observation-panel">
            <div className="observation-number">{(correlation.combined_df || []).length.toLocaleString()}</div>
            <span className="snapshot-label">Common observations</span>
            <p>Correlation is calculated only where every selected index has a return observation for the chosen interval.</p>
          </Panel>
        </div>
      )}
      {!loading && !correlation && !error && <EmptyState title="Select at least two indexes" detail="Choose the series you want to analyze above." />}
    </>
  )
}

function PortfolioTestingView({ indexes, filters }) {
  const [components, setComponents] = useState([])
  const [rebalancing, setRebalancing] = useState('buy_and_hold')
  const [correlationInterval, setCorrelationInterval] = useState('month')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!indexes.length || components.length) return
    const defaults = [
      ['bovespa', 50],
      ['imab', 30],
      ['sp500brl', 20],
    ].filter(([name]) => indexes.includes(name))
    const initial = defaults.length >= 2 ? defaults : indexes.slice(0, 3).map((name, index) => [name, index === 0 ? 60 : index === 1 ? 40 : 0])
    setComponents(initial.map(([index, weight], id) => ({ id, index, weight })))
  }, [indexes, components.length])

  const totalWeight = components.reduce((total, component) => total + Number(component.weight || 0), 0)
  const isValid = components.length > 0 && components.every((component) => component.index) && Math.abs(totalWeight - 100) < 0.01
  const selectedIndexes = components.map((component) => component.index)

  const updateComponent = (id, key, value) => {
    setComponents((current) => current.map((component) => component.id === id ? { ...component, [key]: key === 'weight' ? value : value } : component))
  }

  const addComponent = () => {
    const nextIndex = indexes.find((name) => !selectedIndexes.includes(name))
    if (!nextIndex) return
    setComponents((current) => [...current, { id: Date.now(), index: nextIndex, weight: 0 }])
  }

  const removeComponent = (id) => {
    if (components.length <= 1) return
    setComponents((current) => current.filter((component) => component.id !== id))
    setResult(null)
  }

  const runTest = () => {
    if (!isValid) return
    setLoading(true)
    setError('')
    setResult(null)
    api.testPortfolio(
      components.map(({ index, weight }) => ({ index, weight: Number(weight) })),
      rebalancing,
      correlationInterval,
      filters,
    )
      .then(setResult)
      .catch((reason) => setError(reason.message))
      .finally(() => setLoading(false))
  }

  const drawdownRows = result?.drawdown?.drawdown || []
  const maxDrawdown = drawdownRows.length ? Math.min(...drawdownRows.map((row) => Number(row.drawdown)).filter(Number.isFinite)) : null
  const riskRows = result?.risk_return?.results_df || []
  const rebalanceLabels = {
    buy_and_hold: 'Buy & hold',
    daily: 'Daily rebalancing',
    monthly: 'Monthly rebalancing',
    yearly: 'Yearly rebalancing',
  }

  return (
    <>
      <div className="portfolio-builder-grid">
        <Panel title="Build your test portfolio" eyebrow="Consumer indexes only" action={<span className={`weight-total ${isValid ? 'valid' : ''}`}>{formatNumber(totalWeight, 0)}% allocated</span>}>
          <div className="portfolio-components">
            {components.map((component, position) => (
              <div className="component-row" key={component.id}>
                <span className="component-number">0{position + 1}</span>
                <select value={component.index} onChange={(event) => updateComponent(component.id, 'index', event.target.value)}>
                  {indexes.filter((name) => name === component.index || !selectedIndexes.includes(name)).map((name) => <option key={name} value={name}>{name}</option>)}
                </select>
                <div className="weight-input"><input type="number" min="0" max="100" step="1" value={component.weight} onChange={(event) => updateComponent(component.id, 'weight', event.target.value)} /><span>%</span></div>
                <button className="remove-component" onClick={() => removeComponent(component.id)} disabled={components.length <= 1} aria-label={`Remove ${component.index}`}>×</button>
              </div>
            ))}
          </div>
          <div className="component-actions">
            <button className="add-component" onClick={addComponent} disabled={components.length >= indexes.length}>+ Add index</button>
            <span className={isValid ? 'allocation-hint valid' : 'allocation-hint'}>{isValid ? 'Ready to test' : 'Weights must add up to 100%'}</span>
          </div>
        </Panel>
        <Panel title="Rebalancing strategy" eyebrow="How the portfolio evolves">
          <div className="strategy-list">
            {[
              ['buy_and_hold', 'Buy & hold', 'Let weights drift with performance'],
              ['daily', 'Daily', 'Restore target weights every session'],
              ['monthly', 'Monthly', 'Restore weights at each month start'],
              ['yearly', 'Yearly', 'Restore weights at each year start'],
            ].map(([value, label, detail]) => (
              <button className={`strategy-option ${rebalancing === value ? 'active' : ''}`} onClick={() => setRebalancing(value)} key={value}>
                <span className="strategy-radio" />
                <span><strong>{label}</strong><small>{detail}</small></span>
              </button>
            ))}
          </div>
          <div className="portfolio-run-row">
            <button className="run-button" onClick={runTest} disabled={!isValid || loading}>{loading ? 'Running test…' : 'Run portfolio test'} <span>→</span></button>
            <span className="run-caption">{rebalanceLabels[rebalancing]}</span>
          </div>
        </Panel>
      </div>
      <div className="portfolio-correlation-controls">
        <span className="eyebrow">Correlation interval</span>
        <div className="segmented-control">{['daily', 'month', 'year'].map((item) => <button className={correlationInterval === item ? 'active' : ''} onClick={() => setCorrelationInterval(item)} key={item}>{item}</button>)}</div>
        <span className="control-note">Used when the test is run</span>
      </div>
      <ErrorBanner message={error} />
      {loading && <LoadingState label="Simulating portfolio and calculating metrics" />}
      {!loading && result && (
        <>
          <div className="metric-grid">
            <MetricCard label="Total return" value={formatPercent(result.rentability?.total_return)} detail={rebalanceLabels[result.rebalancing]} accent="mint" />
            <MetricCard label="CAGR" value={formatPercent(result.rentability?.annualized_return)} detail="Annualized compounded return" accent="gold" />
            <MetricCard label="Portfolio risk" value={`${formatNumber(result.rentability?.annualized_volatility)}%`} detail="Annualized volatility" accent="blue" />
            <MetricCard label="Maximum drawdown" value={`${formatNumber(maxDrawdown)}%`} detail="Peak to trough" accent="pink" />
          </div>
          <div className="overview-grid portfolio-chart-grid">
            <Panel title="Portfolio performance" eyebrow={`${rebalanceLabels[result.rebalancing]} · normalized return`}>
              <LineChart rows={result.rentability?.rentability} valueKey="rentability" />
            </Panel>
            <Panel title="Drawdown profile" eyebrow="Distance from running peak">
              <LineChart rows={drawdownRows} valueKey="drawdown" color="#ef7b9a" />
            </Panel>
          </div>
          <div className="comparison-grid portfolio-results-grid">
            <Panel title="Portfolio vs components" eyebrow="Return and risk by series">
              <AnalysisTable rows={riskRows} columns={[['index', 'Index'], ['total_return', 'Return'], ['annualized_return', 'CAGR'], ['annualized_volatility', 'Risk']]} percentColumns={['total_return', 'annualized_return', 'annualized_volatility']} />
            </Panel>
            <Panel title="Composition" eyebrow="Target allocations">
              <div className="composition-list">{result.components?.map((component, index) => <div className="composition-row" key={component.index}><span><i style={{ backgroundColor: COLORS[index % COLORS.length] }} />{component.index}</span><strong>{formatNumber(component.weight, 0)}%</strong></div>)}</div>
            </Panel>
          </div>
          <Panel title="Correlation with composing indexes" eyebrow={`${correlationInterval} return variation`} className="portfolio-correlation-panel">
            <CorrelationTable rows={result.correlation?.correlation_matrix} />
          </Panel>
        </>
      )}
      {!loading && !result && !error && <EmptyState title="Configure a composition and run the test" detail="The results will include performance, CAGR, risk, drawdown, and correlations." />}
    </>
  )
}

function AnalysisTable({ rows, columns, percentColumns = [] }) {
  if (!rows?.length) return <EmptyState title="No table data" />
  const sorted = [...rows].sort((a, b) => Number(b.annualized_return || b.total_return || 0) - Number(a.annualized_return || a.total_return || 0))
  return (
    <div className="table-scroll">
      <table className="data-table">
        <thead><tr>{columns.map(([, label]) => <th key={label}>{label}</th>)}</tr></thead>
        <tbody>{sorted.map((row) => <tr key={row.index}>{columns.map(([key]) => <td key={key} className={key === 'index' ? 'strong-cell' : ''}>{key === 'index' ? row[key] : percentColumns.includes(key) ? formatPercent(row[key]) : formatNumber(row[key])}</td>)}</tr>)}</tbody>
      </table>
    </div>
  )
}

export default App
