import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { weatherApi, cropsApi, expensesApi, pricesApi, chatApi, authApi, soilApi, dashboardApi } from '../services/api';

// Query keys for cache management
export const queryKeys = {
    weather: (city) => ['weather', city],
    weatherForecast: (city) => ['weather', 'forecast', city],
    crops: ['crops'],
    expenses: ['expenses'],
    expensesSummary: ['expenses', 'summary'],
    prices: (crop, state) => ['prices', crop, state],
    profile: ['profile'],
    soil: ['soil'],
    dashboardInsight: (city, crop) => ['dashboard', 'insight', city, crop],
};

// Weather hooks
export const useWeather = (city) => {
    return useQuery({
        queryKey: queryKeys.weather(city),
        queryFn: () => weatherApi.getWeather(city),
        enabled: !!city && city.length > 2,
        staleTime: 10 * 60 * 1000, // 10 minutes
        retry: 2,
        retryDelay: 1000,
    });
};

export const useWeatherForecast = (city) => {
    return useQuery({
        queryKey: queryKeys.weatherForecast(city),
        queryFn: () => weatherApi.getForecast(city),
        enabled: !!city && city.length > 2,
        staleTime: 10 * 60 * 1000, // 10 minutes
        retry: 2,
        retryDelay: 1000,
    });
};

// Crops hooks
export const useCrops = () => {
    return useQuery({
        queryKey: queryKeys.crops,
        queryFn: cropsApi.getAll,
    });
};

export const useAddCrop = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: cropsApi.add,
        onSuccess: () => {
            // Invalidate and refetch crops
            queryClient.invalidateQueries({ queryKey: queryKeys.crops });
        },
        onError: (error) => {
            console.error('Failed to add crop:', error);
            const message = error?.response?.data?.detail || 'Failed to add crop. Please try again.';
            alert(`Error: ${message}`);
        },
    });
};

export const useDeleteCrop = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: cropsApi.delete,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.crops });
        },
        onError: (error) => {
            console.error('Failed to delete crop:', error);
            const message = error?.response?.data?.detail || 'Failed to delete crop. Please try again.';
            alert(`Error: ${message}`);
        },
    });
};

export const useUpdateCropStage = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, stage }) => cropsApi.updateStage(id, stage),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.crops });
        },
        onError: (error) => {
            console.error('Failed to update crop stage:', error);
            const message = error?.response?.data?.detail || 'Failed to update crop stage. Please try again.';
            alert(`Error: ${message}`);
        },
    });
};

// Expenses hooks
export const useExpenses = () => {
    return useQuery({
        queryKey: queryKeys.expenses,
        queryFn: expensesApi.getAll,
    });
};

export const useExpensesSummary = () => {
    return useQuery({
        queryKey: queryKeys.expensesSummary,
        queryFn: expensesApi.getSummary,
    });
};

export const useAddExpense = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: expensesApi.add,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.expenses });
            queryClient.invalidateQueries({ queryKey: queryKeys.expensesSummary });
        },
        onError: (error) => {
            console.error('Failed to add expense:', error);
            const message = error?.response?.data?.detail || 'Failed to add expense. Please try again.';
            alert(`Error: ${message}`);
        },
    });
};

export const useDeleteExpense = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: expensesApi.delete,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.expenses });
            queryClient.invalidateQueries({ queryKey: queryKeys.expensesSummary });
        },
        onError: (error) => {
            console.error('Failed to delete expense:', error);
            const message = error?.response?.data?.detail || 'Failed to delete expense. Please try again.';
            alert(`Error: ${message}`);
        },
    });
};

// Prices hooks
export const usePrices = (crop, state) => {
    return useQuery({
        queryKey: queryKeys.prices(crop, state),
        queryFn: () => pricesApi.getPrice(crop, state),
        enabled: !!crop && !!state,
        staleTime: 30 * 60 * 1000, // 30 minutes - prices don't change often
    });
};

// Chat hooks
export const useSendMessage = () => {
    return useMutation({
        mutationFn: (data) => chatApi.sendMessage(data),
    });
};

// Auth hooks
export const useProfile = () => {
    return useQuery({
        queryKey: queryKeys.profile,
        queryFn: authApi.getProfile,
        retry: false,
    });
};

// Soil hooks
export const useSoilReports = () => {
    return useQuery({
        queryKey: queryKeys.soil,
        queryFn: soilApi.getAll,
    });
};

export const useAddSoilReport = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: soilApi.add,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.soil });
        },
        onError: (error) => {
            console.error('Failed to add soil report:', error);
            const message = error?.response?.data?.detail || 'Failed to add soil report. Please try again.';
            alert(`Error: ${message}`);
        },
    });
};

// Dashboard hooks
export const useDashboardInsight = (city = 'Pune', crop = 'Tomato') => {
    return useQuery({
        queryKey: queryKeys.dashboardInsight(city, crop),
        queryFn: () => dashboardApi.getInsight(city, crop),
        staleTime: 15 * 60 * 1000, // 15 minutes
        retry: 2,
    });
};
