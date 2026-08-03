import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import threading
import math
import random

# --- CONFIGURATION ---
API_KEY = "1ff13315fef13eb12637224376602890"

class WeatherCanvas(tk.Canvas):
    """Animated weather display using Tkinter Canvas."""
    def __init__(self, parent, width=360, height=160, bg="#87CEEB"):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0)
        self.weather_type = "clear"
        self.particles = []
        self.clouds = [
            [float(random.randint(0, 360)), float(random.randint(10, 60))] for _ in range(3)
        ]
        self.angle = 0
        self.flash_counter = 0
        self.flash_alpha = 0
        self.after(50, self.animate)

    def set_weather(self, weather_type):
        """Change the animation type and reset state."""
        self.weather_type = weather_type
        self.particles = []
        self.clouds = [
            [float(random.randint(-40, 360)), float(random.randint(10, 60))] for _ in range(3)
        ]
        self.flash_counter = 0
        self.flash_alpha = 0
        self.configure(bg=self.get_bg_color())

    def get_bg_color(self):
        if self.weather_type == "thunderstorm":
            return "#2F3B4C"
        elif self.weather_type == "rain":
            return "#5A6B7C"
        elif self.weather_type == "snow":
            return "#B8C9D9"
        elif self.weather_type == "clouds":
            return "#A9B8C9"
        elif self.weather_type == "fog":
            return "#BFC9CC"
        else:
            return "#87CEEB"

    def animate(self):
        self.delete("all")
        if self.weather_type == "clear":
            self.draw_sun()
            self.draw_drifting_clouds()
        elif self.weather_type == "clouds":
            self.draw_puffy_clouds()
        elif self.weather_type == "rain":
            self.draw_puffy_clouds()
            self.update_rain()
        elif self.weather_type == "snow":
            self.draw_puffy_clouds()
            self.update_snow()
        elif self.weather_type == "thunderstorm":
            self.draw_puffy_clouds()
            self.update_rain()
            self.update_lightning()
        elif self.weather_type == "fog":
            self.draw_fog()
        self.after(50, self.animate)

    def draw_sun(self):
        """Sun with slowly rotating rays."""
        cx, cy, r = 280, 50, 26
        self.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#FFD700", outline="")
        num_rays = 8
        for i in range(num_rays):
            a = math.radians(self.angle + i * 45)
            x1 = cx + (r + 6) * math.cos(a)
            y1 = cy + (r + 6) * math.sin(a)
            x2 = cx + (r + 18) * math.cos(a)
            y2 = cy + (r + 18) * math.sin(a)
            self.create_line(x1, y1, x2, y2, fill="#FFD700", width=3)
        self.angle += 2

    def draw_drifting_clouds(self):
        """Small white clouds drifting across a clear sky."""
        for cloud in self.clouds:
            x, y = cloud
            self.create_oval(x - 18, y, x + 18, y + 12, fill="white", outline="")
            self.create_oval(x - 8, y - 8, x + 20, y + 8, fill="white", outline="")
            self.create_oval(x + 12, y - 4, x + 32, y + 12, fill="white", outline="")
            cloud[0] += 0.6
            cloud[1] += 0.03
            if cloud[0] > 370:
                cloud[0] = -40
                cloud[1] = random.randint(10, 80)

    def draw_puffy_clouds(self):
        """Large puffy grey clouds for cloudy weather."""
        for cloud in self.clouds:
            x, y = cloud
            self.create_oval(x - 30, y + 10, x + 30, y + 30, fill="#E8EDF2", outline="")
            self.create_oval(x - 15, y - 5, x + 30, y + 20, fill="#E8EDF2", outline="")
            self.create_oval(x + 10, y - 5, x + 45, y + 25, fill="#E8EDF2", outline="")
            cloud[0] += 0.3
            if cloud[0] > 370:
                cloud[0] = -50
                cloud[1] = random.randint(10, 60)

    def update_rain(self):
        """Animated falling rain."""
        if len(self.particles) < 45 or random.random() < 0.4:
            self.particles.append([random.randint(0, 360), random.randint(-20, 0)])
        for p in self.particles:
            x, y = p
            self.create_line(x, y, x - 2, y + 10, fill="#4F8FF0", width=2)
            p[0] += -1.5
            p[1] += 6
            if p[1] > 170 or p[0] < -5:
                p[0] = random.randint(0, 360)
                p[1] = random.randint(-20, 0)

    def update_snow(self):
        """Animated gently falling and swaying snow."""
        if len(self.particles) < 30:
            self.particles.append([random.randint(0, 360), random.randint(-20, 0), random.uniform(0, 2 * math.pi)])
        for p in self.particles:
            x, y, phase = p
            self.create_oval(x, y, x + 7, y + 7, fill="white", outline="white")
            p[0] += math.sin(phase) * 0.8
            p[1] += 1.5
            p[2] += 0.1
            if p[1] > 170:
                p[0] = random.randint(0, 360)
                p[1] = random.randint(-20, 0)
                p[2] = random.uniform(0, 2 * math.pi)

    def update_lightning(self):
        """Random lightning bolts with a flash effect."""
        if random.random() < 0.03:
            self.flash_counter = 3
        if self.flash_counter > 0:
            x = random.randint(100, 260)
            y = 70
            points = [x, y]
            for _ in range(4):
                y += random.randint(20, 40)
                x += random.randint(-25, 25)
                points.extend([x, y])
            self.create_line(points, fill="#FFFF00", width=2)
            self.flash_alpha = 120
            self.flash_counter -= 1
        if self.flash_alpha > 0:
            self.create_rectangle(0, 0, 360, 160, fill="white", stipple="gray25")
            self.flash_alpha -= 25

    def draw_fog(self):
        """Drifting fog patches."""
        for fog in self.clouds:
            x, y = fog
            self.create_oval(x - 40, y + 20, x + 40, y + 40, fill="#D3D8DC", outline="")
            self.create_oval(x - 25, y + 5, x + 35, y + 30, fill="#D3D8DC", outline="")
            fog[0] += 0.8
            fog[1] += 0.02
            if fog[0] > 400:
                fog[0] = -60
                fog[1] = random.randint(20, 80)


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Reporter")
        self.root.geometry("400x600")
        self.root.configure(padx=20, pady=20)

        # UI Elements
        tk.Label(root, text="Enter City Name:", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        self.city_entry = tk.Entry(root, font=("Arial", 12), width=30)
        self.city_entry.pack(pady=5)
        self.city_entry.insert(0, "New York") # Default value

        self.fetch_button = tk.Button(root, text="Get Weather", command=self.start_fetch_thread, 
                                      font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10)
        self.fetch_button.pack(pady=(20, 5))

        # Animated Weather Display
        tk.Label(root, text="Weather Animation:", font=("Arial", 12, "bold")).pack(pady=(5, 5))
        self.weather_canvas = WeatherCanvas(root, width=360, height=160)
        self.weather_canvas.pack(pady=5)

        # Results Display Area
        tk.Label(root, text="Weather Details:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        self.result_text = tk.Text(root, height=8, width=40, font=("Courier", 10), wrap="word")
        self.result_text.pack(pady=5)
        self.result_text.config(state="disabled") # Make it read-only initially

    def update_display(self, text):
        """Helper to update the text area."""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.INSERT, text)
        self.result_text.config(state="disabled")

    def map_weather_condition(self, weather_id, main_cond, desc):
        """Map API weather condition codes/text to an animation type."""
        if weather_id is not None:
            if 200 <= weather_id < 300:
                return "thunderstorm"
            elif 300 <= weather_id < 600:
                return "rain"
            elif 600 <= weather_id < 700:
                return "snow"
            elif 700 <= weather_id < 800:
                return "fog"
            elif weather_id == 800:
                return "clear"
            elif weather_id > 800:
                return "clouds"

        # Fallback to text-based mapping
        main_lower = (main_cond or "").lower()
        desc_lower = (desc or "").lower()
        combined = f"{main_lower} {desc_lower}"
        if "thunder" in combined or "storm" in combined:
            return "thunderstorm"
        elif "snow" in combined:
            return "snow"
        elif "rain" in combined or "drizzle" in combined:
            return "rain"
        elif "fog" in combined or "mist" in combined or "haze" in combined:
            return "fog"
        elif "cloud" in combined:
            return "clouds"
        else:
            return "clear"

    def start_fetch_thread(self):
        """Starts a new thread to fetch data so the GUI doesn't freeze."""
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        
        # Disable button while loading
        self.fetch_button.config(state="disabled", text="Fetching...")
        
        thread = threading.Thread(target=self.get_weather, args=(city,))
        thread.start()

    def get_weather(self, city_name):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        full_url = f"{base_url}q={city_name}&appid={API_KEY}&units=imperial"

        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                main = data['main']
                weather_main = data['weather'][0]['main']
                weather_id = data['weather'][0].get('id')
                weather_desc = data['weather'][0]['description']
                temp = main['temp']
                feels_like = main['feels_like']
                humidity = main['humidity']
                pressure = main['pressure']
                wind_speed = data['wind']['speed']

                sunrise_ts = data.get('sys', {}).get('sunrise')
                sunset_ts = data.get('sys', {}).get('sunset')
                sunrise = datetime.fromtimestamp(sunrise_ts).strftime('%I:%M %p') if sunrise_ts else "N/A"
                sunset = datetime.fromtimestamp(sunset_ts).strftime('%I:%M %p') if sunset_ts else "N/A"

                result_str = (
                    f"--- Weather in {city_name.upper()} ---\n"
                    f"Condition:    {weather_desc.capitalize()}\n"
                    f"Temperature:  {temp}°F (Feels like: {feels_like}°F)\n"
                    f"Humidity:     {humidity}%\n"
                    f"Wind Speed:   {wind_speed} mph\n"
                    f"Pressure:      {pressure} hPa\n"
                    f"Sunrise:       {sunrise}\n"
                    f"Sunset:        {sunset}"
                )
                # Map weather to animation and update UI from the thread safely
                anim_type = self.map_weather_condition(weather_id, weather_main, weather_desc)
                self.root.after(0, lambda: self.weather_canvas.set_weather(anim_type))
                self.root.after(0, self.update_display, result_str)
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "City not found or API error."))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Connection failed: {e}"))
        finally:
            # Re-enable the button regardless of success/failure
            self.root.after(0, lambda: self.fetch_button.config(state="normal", text="Get Weather"))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()