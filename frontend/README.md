# EcoVision: Climate Visualizer Frontend

Luckily, one of your coworkers helped build this frontend for the EcoVision Climate Visualizer application. 

They built it with today's modern stacks: React, Vite, and TailwindCSS. The visualization components are pre-implemented, but they don't quite know how to wire it all up together. 

<small>Note: Of course, you're more than welcome to start from scratch, if their boilerplate is not up to your standard...</small>

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

This will start the frontend application at http://localhost:3000.

## Project Structure

- `src/App.jsx` - Main application component, handles state and data flow
- `src/components/` - Pre-implemented React components
  - `Filters.jsx` - Filtering UI with support for quality thresholds
  - `ChartContainer.jsx` - Pre-built chart visualization component
  - `QualityIndicator.jsx` - Data quality distribution display
  - `TrendAnalysis.jsx` - Trend and anomaly visualization

## Your Tasks

Focus on implementing:

1. API Integration
   - Implement API calls in your preferred way (fetch, custom hooks, etc.)
   - Handle API responses and errors appropriately
   - Map API data to the component props

2. State Management
   - Manage filter state and API parameters
   - Handle loading states during API calls
   - Maintain data consistency across components

3. Data Flow
   - Connect filter changes to API calls
   - Update visualizations when new data arrives
   - Handle empty states and error conditions

## Pre-implemented Features

The following features are already implemented for you:

- Chart visualizations (line and bar charts)
- Quality-weighted data display
- Trend analysis visualization
- Data quality indicators
- Responsive layout and styling
- Loading and empty states

## Component Props

### ChartContainer
```jsx
<ChartContainer 
  title="string"          // Chart title
  loading={boolean}       // Loading state
  chartType="line"|"bar"  // Chart type
  data={array}           // Climate data array
  showQuality={boolean}  // Whether to show quality indicators
/>
```

### QualityIndicator
```jsx
<QualityIndicator 
  data={array}          // Climate data array
  className="string"    // Optional CSS classes
/>
```

### TrendAnalysis
```jsx
<TrendAnalysis 
  data={object}         // Trend analysis data
  loading={boolean}     // Loading state
/>
```

### Filters
```jsx
<Filters 
  locations={array}     // Available locations
  metrics={array}       // Available metrics
  filters={object}      // Current filter values
  onFilterChange={func} // Filter change handler
  onApplyFilters={func} // Apply filters handler
/>
```

## Dependencies

- React - UI library
- Vite - Build tool and dev server
- TailwindCSS - Utility-first CSS framework
- Chart.js and react-chartjs-2 - Pre-configured for visualizations
- React DatePicker - Date selection component

## API Integration Example

```javascript
// Example of fetching climate data
const fetchClimateData = async (filters) => {
  try {
    const queryParams = new URLSearchParams({
      location_id: filters.locationId,
      start_date: filters.startDate,
      end_date: filters.endDate,
      metric: filters.metric,
      quality_threshold: filters.qualityThreshold
    });

    const response = await fetch(`/api/v1/climate?${queryParams}`);
    const data = await response.json();
    
    return data;
  } catch (error) {
    console.error('Error fetching climate data:', error);
    throw error;
  }
};
```

## Implementation Notes

- Focus on clean, maintainable API integration code
- Try to implement proper error handling
- Consider edge cases in data handling
- Follow REST API best practices
- Use TypeScript if you prefer (optional)