import traci
import time

def run_digital_twin():
    # 1. Connect to the already running SUMO-GUI
    # Ensure you launch SUMO with: sumo-gui -c osm.sumocfg --remote-port 8888
    traci.init(8888) 
    
    print("🚀 Digital Twin Bridge Active. Monitoring SRM Campus Traffic...")

    try:
        step = 0
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            
            # 2. Get all active Vehicle IDs (your IoT Entities)
            vehicles = traci.vehicle.getIDList()
            
            for veh_id in vehicles:
                # Get GPS-like coordinates (Longitude, Latitude)
                # This is what we will send to Three.js
                lon, lat = traci.vehicle.getPosition(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                
                # In a real Nokia demo, this is where we'd poll the 5G Core
                # For now, let's print the "Digital Twin" state
                print(f"Step {step} | ID: {veh_id} | Pos: ({lon:.6f}, {lat:.6f}) | Speed: {speed:.2f} m/s")
                
                # Phase 3 Logic Hint:
                # if speed < 2.0: 
                #    trigger_5g_slice_optimization(veh_id)
            
            step += 1
            time.sleep(0.1) # Slow down for visibility
            
    except Exception as e:
        print(f"Connection lost: {e}")
    finally:
        traci.close()

if __name__ == "__main__":
    run_digital_twin()
