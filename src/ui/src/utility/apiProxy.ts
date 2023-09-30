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
          
          console.log(`[APIProxy] Response received with status: ${response.status}`);

          const data = await response.json();
          console.log(`[APIProxy] Parsed response JSON:`, data);

          if (response.ok) {
              console.log(`[APIProxy] Request was successful.`);
              return { success: true, data };
          } else {
              console.warn(`[APIProxy] Response indicates a failure.`);
              return { success: false, error: data.message || 'Error occurred.' };
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
