export class APIProxy {
  private baseURL: string = 'https://api.dev.io:5000';
  private defaultHeaders = {
      'Content-Type': 'application/json',
  };

  constructor() {
      this.fetchEndpoint = this.fetchEndpoint.bind(this);
  }

  async fetchEndpoint(endpoint: string, options: RequestInit) {
      console.log(`[APIProxy] Preparing to call endpoint: ${this.baseURL}${endpoint}`);
      console.log(`[APIProxy] With options:`, options);

      try {
          const fullUrl = `${this.baseURL}${endpoint}`;
          console.log(`[APIProxy] Initiating fetch to: ${fullUrl}`);

          const response = await fetch(fullUrl, {
              ...options,
              headers: {
                  ...this.defaultHeaders,
                  ...options.headers,
              }
          });

          const headersObj: Record<string, string> = {};
          const entriesArray = Array.from(response.headers.entries());
          entriesArray.forEach(([key, value]) => {
              headersObj[key] = value;
          });
          console.log('[APIProxy] Response headers:', headersObj);
          


          console.log('[APIProxy] Full response object:', response);

          const responseBody = await response.text();
          console.log('[APIProxy] Response body:', responseBody);

          // Handle redirects
          if (response.status >= 300 && response.status < 400) {
              const location = response.headers.get('Location');
              console.warn(`[APIProxy] Redirect detected to: ${location}`);
              return { success: false, redirect: true, location };
          }

          // Additional error handling for other status codes
          if (response.status === 404) {
              return { success: false, error: 'Resource not found.' };
          }
          if (response.status >= 500) {
              return { success: false, error: 'Server error. Please try again later.' };
          }

          let parsedData = null;
          if (response.headers.get('content-type')?.includes('application/json')) {
              try {
                  parsedData = JSON.parse(responseBody);
                  console.log(`[APIProxy] Parsed response JSON:`, parsedData);
              } catch (parseError) {
                  console.error('[APIProxy] Error parsing response JSON:', parseError);
                  return { success: false, error: 'Error occurred during JSON parsing.' };
              }

              if (response.ok) {
                  console.log(`[APIProxy] Request was successful.`);
                  return { success: true, data: parsedData };
              } else {
                  console.warn(`[APIProxy] Response indicates a failure.`);
                  return { success: false, error: parsedData.message || 'Error occurred.' };
              }
          } else {
              // No content or not JSON, handle appropriately
              if (response.ok) {
                  return { success: true };
              } else {
                  console.warn(`[APIProxy] Response indicates a failure but no JSON data.`);
                  return { success: false, error: 'Error occurred.' };
              }
          }
      } catch (error) {
          console.error(`[APIProxy] Exception caught during fetch:`, error);
          if (error instanceof Error) {
              return { success: false, error: error.message || 'An error occurred.' };
          }
          return { success: false, error: 'An error occurred.' };
      }
  }
}
