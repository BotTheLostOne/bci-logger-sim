"""
Mock Game Loop Example
=======================

Demonstrates integration with a neural-DnD game using intuition rolls.
This example simulates a game session where characters make intuition checks
backed by neural signal generation.
"""

import sys
import os
import time

# Add parent directory to path to import bci_logger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bci_logger import BrainModel, IntuitionRollAPI


def print_separator():
    print("-" * 60)


def main():
    print("=" * 60)
    print("Neural-DnD Game - Mock Game Loop")
    print("=" * 60)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Initialize game with BCI integration
    print("\n>>> Initializing neural-DnD game engine...")
    
    brain_model = BrainModel(n_neurons=50, seed=42)
    intuition_api = IntuitionRollAPI(
        brain_model=brain_model,
        enable_logging=True,
        log_dir="output"
    )
    
    print("    Neural interface ready!")
    
    # Define callbacks for game events
    def on_critical_success(data):
        print(f"\n    🎉 CRITICAL SUCCESS! {data['character_name']} rolled a natural 20!")
    
    def on_critical_failure(data):
        print(f"\n    💀 CRITICAL FAILURE! {data['character_name']} rolled a natural 1!")
    
    # Register callbacks
    intuition_api.register_callback("critical_success", on_critical_success)
    intuition_api.register_callback("critical_failure", on_critical_failure)
    
    # Define party of adventurers
    party = [
        {"name": "Gandalf", "wisdom": 18, "class": "Wizard"},
        {"name": "Legolas", "wisdom": 14, "class": "Ranger"},
        {"name": "Gimli", "wisdom": 10, "class": "Fighter"},
        {"name": "Frodo", "wisdom": 12, "class": "Rogue"}
    ]
    
    print(f"\n>>> Party of {len(party)} adventurers assembled:")
    for character in party:
        print(f"    - {character['name']} ({character['class']}) - Wisdom: {character['wisdom']}")
    
    # Game scenarios
    scenarios = [
        {
            "context": "You enter a dark cave. Something feels off...",
            "difficulty": 12,
            "description": "Detect hidden trap"
        },
        {
            "context": "The merchant's smile seems too friendly...",
            "difficulty": 15,
            "description": "Sense motive"
        },
        {
            "context": "Footprints lead in multiple directions...",
            "difficulty": 10,
            "description": "Track the right path"
        },
        {
            "context": "Ancient runes glow faintly on the wall...",
            "difficulty": 18,
            "description": "Understand magical warning"
        }
    ]
    
    print("\n>>> Starting adventure...")
    print_separator()
    
    # Game loop
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n[Scene {i}]")
        print(f"Context: {scenario['context']}")
        print(f"Required: {scenario['description']} (DC {scenario['difficulty']})")
        print()
        
        # Each party member makes an intuition check
        for character in party:
            print(f"  {character['name']} focuses their mind...")
            
            # Simulate thinking time
            time.sleep(0.1)
            
            # Make intuition check with neural signal generation
            result = intuition_api.intuition_check(
                character_name=character['name'],
                wisdom=character['wisdom'],
                difficulty=scenario['difficulty'],
                context=scenario['description'],
                duration=0.5  # 500ms of neural activity
            )
            
            check = result['intuition_check']
            neural = result['neural_summary']
            
            # Display results
            roll_str = f"d20: {check['d20_roll']}"
            if check['wisdom_modifier'] >= 0:
                roll_str += f" + {check['wisdom_modifier']}"
            else:
                roll_str += f" - {abs(check['wisdom_modifier'])}"
            roll_str += f" = {check['total_score']}"
            
            outcome = "SUCCESS" if check['success'] else "FAILURE"
            symbol = "✓" if check['success'] else "✗"
            
            print(f"    {symbol} {roll_str} | {outcome}")
            print(f"       Neural state: {neural['state']} | Spikes: {neural['total_spikes']}")
        
        print_separator()
        
        # Brief pause between scenarios
        time.sleep(0.2)
    
    # End of game - show statistics
    print("\n>>> Adventure completed!")
    print("\n>>> Session Statistics:")
    
    stats = intuition_api.get_statistics()
    print(f"    Total checks: {stats['total_checks']}")
    print(f"    Success rate: {stats['success_rate']*100:.1f}%")
    print(f"    Average roll: {stats['average_d20_roll']:.1f}")
    print(f"    Critical successes: {stats['critical_success_count']}")
    print(f"    Critical failures: {stats['critical_failure_count']}")
    
    # Save session logs
    print("\n>>> Saving session data...")
    json_path = intuition_api.save_logs(format="json")
    csv_path = intuition_api.save_logs(format="csv")
    
    print(f"    JSON log: {json_path}")
    print(f"    CSV log: {csv_path}")
    
    print("\n" + "=" * 60)
    print("Game session ended. May your dice roll true!")
    print("=" * 60)


if __name__ == "__main__":
    main()
