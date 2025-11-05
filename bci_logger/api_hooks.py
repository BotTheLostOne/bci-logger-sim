"""
API Hooks Module
================

Provides API hooks for integrating BCI signals with gaming applications.
Specifically designed for neural-DnD game with 'intuition rolls'.
"""

from typing import Dict, Any, Optional, Callable
from .brain_model import BrainModel
from .logger import JSONLogger, CSVLogger


class IntuitionRollAPI:
    """
    API for integrating BCI-based intuition rolls into gaming applications.
    
    Provides hooks for D&D-style intuition checks backed by neural signals.
    """
    
    def __init__(
        self,
        brain_model: Optional[BrainModel] = None,
        enable_logging: bool = True,
        log_dir: str = "logs"
    ):
        """
        Initialize the Intuition Roll API.
        
        Args:
            brain_model: BrainModel instance (creates default if None)
            enable_logging: Whether to enable automatic logging
            log_dir: Directory for log files
        """
        self.brain_model = brain_model or BrainModel(n_neurons=50)
        self.enable_logging = enable_logging
        self.log_dir = log_dir
        
        if enable_logging:
            self.json_logger = JSONLogger(output_dir=log_dir)
            self.csv_logger = CSVLogger(output_dir=log_dir)
        
        # Callback registry
        self.callbacks = {
            "pre_roll": [],
            "post_roll": [],
            "critical_success": [],
            "critical_failure": []
        }
    
    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register a callback function for an event.
        
        Args:
            event: Event name ('pre_roll', 'post_roll', 'critical_success', 'critical_failure')
            callback: Callback function to execute
        """
        if event not in self.callbacks:
            raise ValueError(f"Unknown event: {event}")
        
        self.callbacks[event].append(callback)
    
    def _trigger_callbacks(self, event: str, data: Dict[str, Any]) -> None:
        """Execute all callbacks for an event."""
        for callback in self.callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                print(f"Callback error for {event}: {e}")
    
    def intuition_check(
        self,
        character_name: str,
        wisdom: int,
        difficulty: int,
        context: Optional[str] = None,
        duration: float = 1.0
    ) -> Dict[str, Any]:
        """
        Perform an intuition check with neural signal generation.
        
        Args:
            character_name: Name of the character
            wisdom: Wisdom score (1-30)
            difficulty: Difficulty class (1-30)
            context: Optional context description
            duration: Duration of neural activity in seconds
            
        Returns:
            Dictionary with check results and neural data
        """
        # Trigger pre-roll callbacks
        pre_data = {
            "character_name": character_name,
            "wisdom": wisdom,
            "difficulty": difficulty,
            "context": context
        }
        self._trigger_callbacks("pre_roll", pre_data)
        
        # Generate neural signals for intuition
        neural_data = self.brain_model.generate_intuition_signal(
            difficulty=difficulty,
            character_wisdom=wisdom,
            duration=duration
        )
        
        intuition_result = neural_data["intuition_data"]
        
        # Build result
        result = {
            "character_name": character_name,
            "intuition_check": intuition_result,
            "context": context,
            "neural_summary": {
                "state": neural_data["state"],
                "n_neurons": neural_data["n_neurons"],
                "total_spikes": sum(s["spike_count"] for s in neural_data["spike_trains"]),
                "duration": duration
            }
        }
        
        # Check for critical results
        if intuition_result["d20_roll"] == 20:
            self._trigger_callbacks("critical_success", result)
        elif intuition_result["d20_roll"] == 1:
            self._trigger_callbacks("critical_failure", result)
        
        # Trigger post-roll callbacks
        self._trigger_callbacks("post_roll", result)
        
        # Log if enabled
        if self.enable_logging:
            self.json_logger.log(result)
        
        return result
    
    def batch_intuition_checks(
        self,
        checks: list[Dict[str, Any]]
    ) -> list[Dict[str, Any]]:
        """
        Perform multiple intuition checks in batch.
        
        Args:
            checks: List of check parameters (each with character_name, wisdom, difficulty)
            
        Returns:
            List of check results
        """
        results = []
        
        for check in checks:
            result = self.intuition_check(
                character_name=check.get("character_name", "Unknown"),
                wisdom=check.get("wisdom", 10),
                difficulty=check.get("difficulty", 10),
                context=check.get("context"),
                duration=check.get("duration", 1.0)
            )
            results.append(result)
        
        return results
    
    def save_logs(self, format: str = "json") -> str:
        """
        Save logged data to file.
        
        Args:
            format: Output format ('json' or 'csv')
            
        Returns:
            Path to saved file
        """
        if not self.enable_logging:
            raise RuntimeError("Logging is not enabled")
        
        if format == "json":
            return self.json_logger.save()
        elif format == "csv":
            # Convert logged entries to summary format
            summary_data = []
            for entry in self.json_logger.log_entries:
                summary_entry = {
                    "character_name": entry.get("character_name"),
                    "d20_roll": entry["intuition_check"]["d20_roll"],
                    "wisdom_modifier": entry["intuition_check"]["wisdom_modifier"],
                    "total_score": entry["intuition_check"]["total_score"],
                    "difficulty": entry["intuition_check"]["difficulty_class"],
                    "success": entry["intuition_check"]["success"],
                    "state": entry["neural_summary"]["state"],
                    "total_spikes": entry["neural_summary"]["total_spikes"],
                    "context": entry.get("context", "")
                }
                summary_data.append(summary_entry)
            
            return self.csv_logger.save_summary(summary_data, "intuition_checks.csv")
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics from all logged intuition checks.
        
        Returns:
            Dictionary with statistics
        """
        if not self.enable_logging or not self.json_logger.log_entries:
            return {
                "total_checks": 0,
                "success_rate": 0.0,
                "critical_success_rate": 0.0,
                "critical_failure_rate": 0.0
            }
        
        entries = self.json_logger.log_entries
        total = len(entries)
        
        successes = sum(1 for e in entries if e["intuition_check"]["success"])
        nat_20s = sum(1 for e in entries if e["intuition_check"]["d20_roll"] == 20)
        nat_1s = sum(1 for e in entries if e["intuition_check"]["d20_roll"] == 1)
        
        avg_roll = sum(e["intuition_check"]["d20_roll"] for e in entries) / total
        avg_total = sum(e["intuition_check"]["total_score"] for e in entries) / total
        
        return {
            "total_checks": total,
            "success_count": successes,
            "success_rate": successes / total,
            "critical_success_count": nat_20s,
            "critical_success_rate": nat_20s / total,
            "critical_failure_count": nat_1s,
            "critical_failure_rate": nat_1s / total,
            "average_d20_roll": avg_roll,
            "average_total_score": avg_total
        }
