# ⚡ KisanAI - React Query Optimization Guide

> **Purpose:** Best practices for React Query, performance optimization, and state management patterns.

---

## 📋 Table of Contents

1. [React Query Configuration](#react-query-configuration)
2. [Query Patterns](#query-patterns)
3. [Mutation Patterns](#mutation-patterns)
4. [Cache Management](#cache-management)
5. [Error Handling](#error-handling)
6. [Performance Optimization](#performance-optimization)
7. [Custom Hooks](#custom-hooks)

---

## ⚙️ React Query Configuration

### Current Configuration (`lib/queryClient.js`)

```javascript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,        // 5 minutes - data stays fresh
      cacheTime: 10 * 60 * 1000,       // 10 minutes - cache retention
      retry: 1,                         // Retry failed requests once
      refetchOnWindowFocus: import.meta.env.PROD, // Only in production
      refetchOnReconnect: true,         // Refetch on internet reconnection
    },
    mutations: {
      retry: 1,                         // Retry failed mutations once
      onError: (error) => {
        console.error('Mutation error:', error);
      },
    },
  },
});
```

### Recommended: Per-Feature Configuration

```javascript
// lib/queryClient.js - Enhanced
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      cacheTime: 10 * 60 * 1000,
      retry: (failureCount, error) => {
        // Don't retry on 4xx errors (client errors)
        if (error.response?.status >= 400 && error.response?.status < 500) {
          return false;
        }
        return failureCount < 2;  // Max 2 retries for 5xx errors
      },
      refetchOnWindowFocus: import.meta.env.PROD,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 0,  // Don't retry mutations by default
    },
  },
});

// Feature-specific stale times
export const STALE_TIME = {
  SHORT: 1 * 60 * 1000,      // 1 minute - frequently changing data
  MEDIUM: 5 * 60 * 1000,     // 5 minutes - default
  LONG: 15 * 60 * 1000,      // 15 minutes - slow-changing data
  VERY_LONG: 30 * 60 * 1000, // 30 minutes - static-like data
};
```

---

## 🔍 Query Patterns

### Basic Query Pattern

```javascript
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';

// ❌ Bad - no key array, inconsistent structure
const { data, isLoading, error } = useQuery('crops', () => api.get('/crops'));

// ✅ Good - proper key array, explicit typing
const { data, isLoading, error } = useQuery({
  queryKey: ['crops'],
  queryFn: () => api.get('/crops').then(res => res.data),
  staleTime: STALE_TIME.MEDIUM,
});
```

### Query with Parameters

```javascript
// ✅ Include all parameters in queryKey
function useCrop(cropId) {
  return useQuery({
    queryKey: ['crops', cropId],  // Key includes parameter
    queryFn: () => api.get(`/crops/${cropId}`).then(res => res.data),
    enabled: !!cropId,  // Only run if cropId exists
  });
}

// ✅ Query with multiple parameters
function useWeatherForecast(city, days = 5) {
  return useQuery({
    queryKey: ['weather', 'forecast', city, days],
    queryFn: () => api.get(`/weather/forecast?city=${city}&days=${days}`).then(res => res.data),
    enabled: !!city && city.length > 0,
    staleTime: STALE_TIME.LONG,  // Weather doesn't change quickly
  });
}
```

### Dependent Queries

```javascript
// ✅ Query that depends on another query
function useCropExpenses(cropId) {
  const { data: crop, isLoading: cropLoading } = useCrop(cropId);
  
  const { data: expenses, isLoading: expensesLoading } = useQuery({
    queryKey: ['expenses', 'crop', cropId],
    queryFn: () => api.get(`/expenses?crop_id=${cropId}`).then(res => res.data),
    enabled: !!crop,  // Only fetch expenses if crop exists
  });
  
  return {
    crop,
    expenses,
    isLoading: cropLoading || expensesLoading,
  };
}
```

### Parallel Queries

```javascript
import { useQueries } from '@tanstack/react-query';

// ✅ Fetch multiple resources in parallel
function useDashboardData() {
  const results = useQueries({
    queries: [
      {
        queryKey: ['weather'],
        queryFn: () => api.get('/weather').then(res => res.data),
        staleTime: STALE_TIME.LONG,
      },
      {
        queryKey: ['crops'],
        queryFn: () => api.get('/crops').then(res => res.data),
        staleTime: STALE_TIME.MEDIUM,
      },
      {
        queryKey: ['expenses', 'summary'],
        queryFn: () => api.get('/expenses/summary').then(res => res.data),
        staleTime: STALE_TIME.SHORT,
      },
    ],
  });

  return {
    weather: results[0].data,
    crops: results[1].data,
    expenses: results[2].data,
    isLoading: results.some(r => r.isLoading),
    error: results.find(r => r.error)?.error,
  };
}
```

---

## 🔄 Mutation Patterns

### Basic Mutation

```javascript
import { useMutation, useQueryClient } from '@tanstack/react-query';

// ✅ Mutation with automatic cache invalidation
function useAddCrop() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (cropData) => api.post('/crops/add', cropData).then(res => res.data),
    onSuccess: () => {
      // Invalidate and refetch crops query
      queryClient.invalidateQueries({ queryKey: ['crops'] });
    },
    onError: (error) => {
      console.error('Failed to add crop:', error);
      // Show toast notification here
    },
  });
}

// Usage in component
function CropForm() {
  const addCrop = useAddCrop();
  
  const handleSubmit = (data) => {
    addCrop.mutate(data, {
      onSuccess: () => {
        toast.success('Crop added successfully');
        closeModal();
      },
    });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <Button 
        type="submit" 
        loading={addCrop.isPending}
        disabled={addCrop.isPending}
      >
        {addCrop.isPending ? 'Adding...' : 'Add Crop'}
      </Button>
    </form>
  );
}
```

### Optimistic Updates

```javascript
// ✅ Update UI immediately, rollback on error
function useUpdateCropStage() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, stage }) => 
      api.patch(`/crops/${id}/stage?stage=${stage}`).then(res => res.data),
    
    onMutate: async ({ id, stage }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['crops'] });
      
      // Snapshot previous value
      const previousCrops = queryClient.getQueryData(['crops']);
      
      // Optimistically update
      queryClient.setQueryData(['crops'], (old) => {
        return old.map(crop => 
          crop.id === id ? { ...crop, stage } : crop
        );
      });
      
      // Return context with snapshot
      return { previousCrops };
    },
    
    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(['crops'], context.previousCrops);
      toast.error('Failed to update stage');
    },
    
    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['crops'] });
    },
  });
}
```

### Multiple Invalidations

```javascript
// ✅ Invalidate multiple related queries
function useDeleteExpense() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id) => api.delete(`/expense/${id}`),
    onSuccess: () => {
      // Invalidate multiple related queries
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      queryClient.invalidateQueries({ queryKey: ['expenses', 'summary'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}
```

---

## 💾 Cache Management

### Manual Cache Updates

```javascript
// ✅ Update cache after successful mutation
function useAddCrop() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (cropData) => api.post('/crops/add', cropData).then(res => res.data),
    onSuccess: (newCrop) => {
      // Option 1: Invalidate (triggers refetch)
      queryClient.invalidateQueries({ queryKey: ['crops'] });
      
      // Option 2: Manual update (no refetch)
      queryClient.setQueryData(['crops'], (old) => {
        return old ? [newCrop, ...old] : [newCrop];
      });
    },
  });
}
```

### Prefetching

```javascript
// ✅ Prefetch data before navigation
function CropList() {
  const queryClient = useQueryClient();
  const { data: crops } = useQuery({
    queryKey: ['crops'],
    queryFn: () => api.get('/crops').then(res => res.data),
  });
  
  const prefetchCropDetails = (cropId) => {
    queryClient.prefetchQuery({
      queryKey: ['crops', cropId],
      queryFn: () => api.get(`/crops/${cropId}`).then(res => res.data),
      staleTime: STALE_TIME.MEDIUM,
    });
  };
  
  return (
    <div>
      {crops?.map(crop => (
        <div
          key={crop.id}
          onMouseEnter={() => prefetchCropDetails(crop.id)}
          onClick={() => navigate(`/crops/${crop.id}`)}
        >
          {crop.name}
        </div>
      ))}
    </div>
  );
}
```

### Cache Hydration

```javascript
// ✅ Set initial cache data from server-side
function App() {
  const queryClient = useQueryClient();
  
  useEffect(() => {
    // Set initial data from localStorage or server
    const cachedCrops = localStorage.getItem('crops');
    if (cachedCrops) {
      queryClient.setQueryData(['crops'], JSON.parse(cachedCrops));
    }
  }, []);
  
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>;
}
```

---

## ⚠️ Error Handling

### Global Error Handling

```javascript
// lib/queryClient.js
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      onError: (error) => {
        if (error.response?.status === 401) {
          // Redirect to login on unauthorized
          window.location.href = '/login';
        } else if (error.response?.status === 500) {
          toast.error('Server error. Please try again later.');
        }
      },
    },
  },
});
```

### Per-Query Error Handling

```javascript
// ✅ Handle errors at component level
function Crops() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['crops'],
    queryFn: () => api.get('/crops').then(res => res.data),
    retry: 2,
  });
  
  if (isLoading) {
    return <SkeletonLoader />;
  }
  
  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">
          {error.response?.data?.detail || 'Failed to load crops'}
        </p>
        <Button onClick={() => refetch()}>
          Try Again
        </Button>
      </div>
    );
  }
  
  return <div>{/* Render data */}</div>;
}
```

---

## ⚡ Performance Optimization

### Avoid Unnecessary Re-renders

```javascript
import { memo, useMemo } from 'react';

// ❌ Bad - re-renders on every parent update
function CropCard({ crop }) {
  return <div>{crop.name}</div>;
}

// ✅ Good - memoized component
const CropCard = memo(function CropCard({ crop }) {
  return <div>{crop.name}</div>;
});

// ✅ Use useMemo for expensive computations
function FinanceAnalytics({ expenses }) {
  const chartData = useMemo(() => {
    // Expensive chart data processing
    return expenses.reduce((acc, exp) => {
      // ... complex logic
      return acc;
    }, []);
  }, [expenses]);
  
  return <Chart data={chartData} />;
}
```

### Select Option for Large Data

```javascript
// ✅ Use select to transform data and prevent re-renders
function useCropNames() {
  return useQuery({
    queryKey: ['crops'],
    queryFn: () => api.get('/crops').then(res => res.data),
    select: (data) => data.map(crop => crop.name), // Only re-render if names change
  });
}

// ✅ Select specific fields
function useCropCount() {
  return useQuery({
    queryKey: ['crops'],
    queryFn: () => api.get('/crops').then(res => res.data),
    select: (data) => data.length, // Component only re-renders if count changes
  });
}
```

### Pagination

```javascript
// ✅ Implement pagination for large lists
function usePaginatedCrops(page = 1, limit = 10) {
  return useQuery({
    queryKey: ['crops', 'paginated', page, limit],
    queryFn: () => 
      api.get(`/crops?skip=${(page - 1) * limit}&limit=${limit}`)
        .then(res => res.data),
    keepPreviousData: true, // Show old data while fetching new page
  });
}

function CropList() {
  const [page, setPage] = useState(1);
  const { data, isPreviousData } = usePaginatedCrops(page, 10);
  
  return (
    <div>
      <div className={isPreviousData ? 'opacity-50' : ''}>
        {data?.crops.map(crop => <CropCard key={crop.id} crop={crop} />)}
      </div>
      
      <div className="flex gap-2">
        <Button 
          onClick={() => setPage(old => Math.max(old - 1, 1))}
          disabled={page === 1}
        >
          Previous
        </Button>
        <Button 
          onClick={() => setPage(old => old + 1)}
          disabled={isPreviousData || !data?.hasMore}
        >
          Next
        </Button>
      </div>
    </div>
  );
}
```

### Infinite Scroll

```javascript
import { useInfiniteQuery } from '@tanstack/react-query';

// ✅ Infinite scroll pattern
function useInfiniteCrops() {
  return useInfiniteQuery({
    queryKey: ['crops', 'infinite'],
    queryFn: ({ pageParam = 0 }) =>
      api.get(`/crops?skip=${pageParam}&limit=10`).then(res => res.data),
    getNextPageParam: (lastPage, pages) => {
      if (lastPage.length < 10) return undefined; // No more pages
      return pages.length * 10; // Next skip value
    },
  });
}

function CropInfiniteList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteCrops();
  
  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.map(crop => <CropCard key={crop.id} crop={crop} />)}
        </div>
      ))}
      
      {hasNextPage && (
        <Button 
          onClick={() => fetchNextPage()}
          loading={isFetchingNextPage}
        >
          Load More
        </Button>
      )}
    </div>
  );
}
```

---

## 🎣 Custom Hooks

### Pattern: Centralized API Hooks

```javascript
// hooks/useApi.js - Current structure (good!)
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { cropsApi, expensesApi, soilApi } from '../services/api';
import { STALE_TIME } from '../lib/queryClient';

// ✅ Crops
export function useCrops() {
  return useQuery({
    queryKey: ['crops'],
    queryFn: cropsApi.getAll,
    staleTime: STALE_TIME.MEDIUM,
  });
}

export function useAddCrop() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: cropsApi.add,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['crops'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}

export function useDeleteCrop() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: cropsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['crops'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}

export function useUpdateCropStage() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, stage }) => cropsApi.updateStage(id, stage),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['crops'] });
    },
  });
}

// ✅ Expenses
export function useExpenses() {
  return useQuery({
    queryKey: ['expenses'],
    queryFn: expensesApi.getAll,
    staleTime: STALE_TIME.SHORT,
  });
}

export function useAddExpense() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: expensesApi.add,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}

export function useDeleteExpense() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: expensesApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}

// ✅ Soil
export function useSoilReports() {
  return useQuery({
    queryKey: ['soil'],
    queryFn: soilApi.getAll,
    staleTime: STALE_TIME.LONG,
  });
}

export function useAddSoilReport() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: soilApi.add,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['soil'] });
    },
  });
}
```

---

## 📊 React Query DevTools

### Setup (Development Only)

```javascript
// main.jsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router />
      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}
```

### Benefits:
- 🔍 Inspect all queries and mutations
- 🕐 See query states (loading, success, error)
- 💾 View cached data
- ♻️ Manually trigger refetch
- 🗑️ Clear specific caches

---

## ✅ Best Practices Checklist

### Query Configuration:
- [ ] Use array queryKeys with all parameters
- [ ] Set appropriate staleTime for each query type
- [ ] Use `enabled` for conditional queries
- [ ] Include `select` for data transformation

### Mutation Configuration:
- [ ] Invalidate related queries after success
- [ ] Show loading states during mutations
- [ ] Handle errors gracefully
- [ ] Consider optimistic updates for instant feedback

### Performance:
- [ ] Memoize expensive computations with useMemo
- [ ] Memoize components with memo
- [ ] Use pagination for large lists
- [ ] Prefetch data before navigation

### Error Handling:
- [ ] Global error boundary
- [ ] Per-query error handling
- [ ] Retry logic configured
- [ ] User-friendly error messages

---

## 🚀 Migration Checklist

If upgrading from old patterns:

1. **Replace direct axios calls:**
   ```javascript
   // ❌ Old
   const [data, setData] = useState(null);
   const [loading, setLoading] = useState(true);
   
   useEffect(() => {
     axios.get('/api/crops').then(res => {
       setData(res.data);
       setLoading(false);
     });
   }, []);
   
   // ✅ New
   const { data, isLoading } = useCrops();
   ```

2. **Replace manual refetching:**
   ```javascript
   // ❌ Old
   const fetchData = () => {
     axios.get('/api/crops').then(...)
   };
   
   // ✅ New
   const { data, refetch } = useCrops();
   ```

3. **Use custom hooks:**
   ```javascript
   // ❌ Old
   const handleAdd = async () => {
     await axios.post('/api/crops', data);
     fetchCrops(); // Manual refetch
   };
   
   // ✅ New
   const addCrop = useAddCrop();
   const handleAdd = () => {
     addCrop.mutate(data); // Auto-invalidates
   };
   ```

---

**Guide Version:** 1.0  
**Last Updated:** November 20, 2025
