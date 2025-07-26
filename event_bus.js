// event_bus.js
const EventEmitter = require('events');
const fs = require('fs');
const path = require('path');

/**
 * Enhanced EventBus for Multi-Agent Coordination
 * Provides pub/sub messaging with persistence and replay capabilities
 */
class AgentEventBus extends EventEmitter {
  constructor(options = {}) {
    super();
    this.logFile = options.logFile || 'agent_events.log';
    this.enablePersistence = options.enablePersistence !== false;
    this.eventHistory = [];
    this.maxHistorySize = options.maxHistorySize || 1000;
    
    // Load existing event history if persistence is enabled
    if (this.enablePersistence) {
      this.loadEventHistory();
    }
    
    console.log('[EventBus] Initialized with persistence:', this.enablePersistence);
  }

  /**
   * Enhanced emit with automatic logging and persistence
   */
  emit(eventName, eventData = {}) {
    const timestamp = new Date().toISOString();
    const eventEntry = {
      timestamp,
      eventName,
      data: eventData,
      id: this.generateEventId()
    };

    // Add to history
    this.eventHistory.push(eventEntry);
    
    // Maintain history size limit
    if (this.eventHistory.length > this.maxHistorySize) {
      this.eventHistory.shift();
    }

    // Persist to file if enabled
    if (this.enablePersistence) {
      this.persistEvent(eventEntry);
    }

    console.log(`[EventBus] 📡 ${eventName}:`, JSON.stringify(eventData));

    // Call parent emit
    return super.emit(eventName, eventData);
  }

  /**
   * Generate unique event ID
   */
  generateEventId() {
    return `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Persist event to log file
   */
  persistEvent(eventEntry) {
    try {
      const logEntry = JSON.stringify(eventEntry) + '\n';
      fs.appendFileSync(this.logFile, logEntry);
    } catch (err) {
      console.warn('[EventBus] Failed to persist event:', err.message);
    }
  }

  /**
   * Load event history from log file
   */
  loadEventHistory() {
    try {
      if (fs.existsSync(this.logFile)) {
        const logContent = fs.readFileSync(this.logFile, 'utf8');
        const lines = logContent.trim().split('\n').filter(line => line.trim());
        
        this.eventHistory = lines.map(line => {
          try {
            return JSON.parse(line);
          } catch {
            return null;
          }
        }).filter(event => event !== null);
        
        console.log(`[EventBus] Loaded ${this.eventHistory.length} events from history`);
      }
    } catch (err) {
      console.warn('[EventBus] Failed to load event history:', err.message);
    }
  }

  /**
   * Get recent events by name
   */
  getRecentEvents(eventName, limit = 10) {
    return this.eventHistory
      .filter(event => event.eventName === eventName)
      .slice(-limit);
  }

  /**
   * Get all events within time range
   */
  getEventsByTimeRange(startTime, endTime) {
    return this.eventHistory.filter(event => {
      const eventTime = new Date(event.timestamp);
      return eventTime >= startTime && eventTime <= endTime;
    });
  }

  /**
   * Replay events to a specific listener
   */
  replayEvents(eventName, listener, fromTime = null) {
    const events = fromTime 
      ? this.getEventsByTimeRange(fromTime, new Date())
      : this.getRecentEvents(eventName);
    
    console.log(`[EventBus] Replaying ${events.length} ${eventName} events`);
    
    events.forEach(event => {
      if (event.eventName === eventName) {
        listener(event.data);
      }
    });
  }

  /**
   * Clear event history
   */
  clearHistory() {
    this.eventHistory = [];
    if (this.enablePersistence && fs.existsSync(this.logFile)) {
      fs.unlinkSync(this.logFile);
    }
    console.log('[EventBus] Event history cleared');
  }

  /**
   * Get event statistics
   */
  getEventStats() {
    const stats = {
      totalEvents: this.eventHistory.length,
      eventTypes: {},
      timeRange: {
        earliest: null,
        latest: null
      }
    };

    this.eventHistory.forEach(event => {
      // Count event types
      stats.eventTypes[event.eventName] = (stats.eventTypes[event.eventName] || 0) + 1;
      
      // Track time range
      const eventTime = new Date(event.timestamp);
      if (!stats.timeRange.earliest || eventTime < stats.timeRange.earliest) {
        stats.timeRange.earliest = eventTime;
      }
      if (!stats.timeRange.latest || eventTime > stats.timeRange.latest) {
        stats.timeRange.latest = eventTime;
      }
    });

    return stats;
  }

  /**
   * Subscribe with automatic replay of recent events
   */
  subscribeWithHistory(eventName, listener, replayCount = 5) {
    // First replay recent events
    const recentEvents = this.getRecentEvents(eventName, replayCount);
    recentEvents.forEach(event => listener(event.data));
    
    // Then subscribe for future events
    this.on(eventName, listener);
    
    console.log(`[EventBus] Subscribed to ${eventName} with ${recentEvents.length} replayed events`);
  }
}

// Create singleton instance
const bus = new AgentEventBus({
  logFile: path.join(__dirname, 'agent_events.log'),
  enablePersistence: true,
  maxHistorySize: 2000
});

// Export both the class and singleton instance
module.exports = bus;
module.exports.AgentEventBus = AgentEventBus;