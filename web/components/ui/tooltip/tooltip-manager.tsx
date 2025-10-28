class TooltipManager {
  private activeCloser: (() => void) | null = null;

  /**
   * Register a tooltip's close function
   * Automatically closes any previously active tooltip
   */
  register(closeFn: () => void) {
    if (this.activeCloser) {
      this.activeCloser();
    }
    this.activeCloser = closeFn;
  }

  /**
   * Clear the reference to a tooltip's close function
   */
  clear(closeFn: () => void) {
    if (this.activeCloser === closeFn) {
      this.activeCloser = null;
    }
  }

  /**
   * Closes the currently active tooltip
   */
  closeActiveTooltip() {
    if (this.activeCloser) {
      this.activeCloser();
      this.activeCloser = null;
    }
  }
}

export const tooltipManager = new TooltipManager();
