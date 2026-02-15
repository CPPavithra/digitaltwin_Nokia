import traci
import asyncio
import websockets
import json
import os

os.environ["SUMO_HOME"] = "/usr/share/sumo"

# Store vehicle data globally so the WebSocket can always access it
latest_data = {}

async def sumo_loop():
    global latest_data
    print("🚦 Connecting to SUMO on port 8888...")
    try:
        traci.init(8888)
        print("✅ SUMO Connected! Waiting for simulation steps...")
        
        step = 0
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            vehicles = traci.vehicle.getIDList()
            
            temp_data = {}
            for veh_id in vehicles:
                x, y = traci.vehicle.getPosition(veh_id)
                angle = traci.vehicle.getAngle(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                
                # Terminal verification (Your favorite part!)
                print(f"Step {step} | ID: {veh_id} | Pos: ({x:.2f}, {y:.2f}) | Speed: {speed:.2f} m/s")
                
                temp_data[veh_id] = {
                    "x": (x / 100) - 65,
                    "y": (y / 100) - 120,
                    "angle": angle,
                    "speed": round(speed, 2)
                }
            latest_data = temp_data
            step += 1
            await asyncio.sleep(0.05)
    except Exception as e:
        print(f"⚠️ SUMO Error: {e}")
    finally:
        traci.close()

async def ws_handler(websocket):
    print("🛰️ Three.js Dashboard Linked to Bridge!")
    try:
        while True:
            if latest_data:
                await websocket.send(json.dumps(latest_data))
            await asyncio.sleep(0.05)
    except websockets.exceptions.ConnectionClosed:
        print("🛑 Dashboard Disconnected.")

async def main():
    # Run both the SUMO client and the WS Server at the same time
    print("🚀 Digital Twin Bridge Launching...")
    server = websockets.serve(ws_handler, "localhost", 8765)
    await asyncio.gather(server, sumo_loop())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bridge Stopped.")
