type ThrottleMap = Map<string, { lastCall: number; timeoutId: NodeJS.Timeout | null }>;

const throttleState: ThrottleMap = new Map();

export const throttleEvent = <T>(
  key: string,
  callback: (data: T) => void,
  data: T,
  delayMs: number = 500
): void => {
  const state = throttleState.get(key);
  const now = Date.now();

  if (!state) {
    // First call
    callback(data);
    throttleState.set(key, { lastCall: now, timeoutId: null });
    return;
  }

  const timeSinceLastCall = now - state.lastCall;

  if (timeSinceLastCall >= delayMs) {
    // Execute immediately
    callback(data);
    state.lastCall = now;
    if (state.timeoutId) {
      clearTimeout(state.timeoutId);
      state.timeoutId = null;
    }
  } else {
    // Schedule for later
    if (state.timeoutId) {
      clearTimeout(state.timeoutId);
    }
    state.timeoutId = setTimeout(() => {
      callback(data);
      state.lastCall = Date.now();
      state.timeoutId = null;
    }, delayMs - timeSinceLastCall);
  }
};

export const clearThrottle = (key: string): void => {
  const state = throttleState.get(key);
  if (state?.timeoutId) {
    clearTimeout(state.timeoutId);
  }
  throttleState.delete(key);
};

export const clearAllThrottles = (): void => {
  throttleState.forEach((state) => {
    if (state.timeoutId) {
      clearTimeout(state.timeoutId);
    }
  });
  throttleState.clear();
};
