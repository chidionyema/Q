import { useState, useCallback } from 'react';

interface ApiResponseSuccess<T> {
  success: true;
  data: T;
  error?: undefined;
}

interface ApiResponseError {
  success: false;
  error: any;
  data?: undefined;
}

type ApiResponse<T> = ApiResponseSuccess<T> | ApiResponseError;

type ApiCallFunc<T> = (endpoint: string, options: RequestInit) => Promise<ApiResponse<T>>;

export type UseApiCallReturnType<T> = {
  call: (endpoint: string, options?: RequestInit) => Promise<T>;
  loading: boolean;
  error: any;
};

export const useApiCall = <T>(apiFunc: ApiCallFunc<T>): UseApiCallReturnType<T> => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<any>(null);

  const call = useCallback(
    async (endpoint: string, options: RequestInit = {}): Promise<T> => {
      console.log(`[useApiCall] Calling endpoint: ${endpoint}`);
      console.log(`[useApiCall] With options:`, options);

      setLoading(true);
      setError(null);
      try {
        console.log(`[useApiCall] Making API call to endpoint:`, endpoint);
        console.log(`[useApiCall] With options:`, options);
        const rawResponse = await apiFunc(endpoint, options);
        console.log(`[useApiCall] Raw response:`, rawResponse);
    
        if (rawResponse.success) {
            setLoading(false);
            return rawResponse.data;
        } else {
            setError(rawResponse.error || 'An error occurred.');
            setLoading(false);
            throw new Error(rawResponse.error || 'An error occurred.');
        }
    } catch (e) {
        console.error(`[useApiCall] Error during API call:`, e);
        setError(e || 'An error occurred.');
        setLoading(false);
        throw e;
    }
    
    
    },
    [apiFunc]
  );

  return {
    call,
    loading,
    error,
  };
};
