import random
import time
from termcolor import colored

class QualityDashboard:
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "errors": 0,
            "avg_latency_ms": 0,
            "critic_scores": []
        }

    def ingest_mock_data(self, num_samples=50):
        """Simulates ingesting trace data from OpenTelemetry/Jaeger"""
        print("📥 Ingesting Trace Data from OpenTelemetry...")
        time.sleep(1)
        
        self.metrics["total_requests"] = num_samples
        self.metrics["errors"] = int(num_samples * 0.04) # 4% error rate
        self.metrics["avg_latency_ms"] = random.randint(800, 1500)
        
        # Simulate Critic Scores (0.0 to 1.0)
        self.metrics["critic_scores"] = [random.uniform(0.8, 1.0) for _ in range(num_samples)]
        # Add a few hallucinations
        for _ in range(3):
            self.metrics["critic_scores"].append(random.uniform(0.4, 0.6))

    def display(self):
        print("\n" + "="*50)
        print(colored(" Athena System - Quality & Observability Dashboard ", "white", "on_blue", attrs=["bold"]))
        print("="*50)
        
        # 1. System Metrics
        print(colored("\n📡 System Metrics", "cyan", attrs=["bold"]))
        print(f"Total Requests: {self.metrics['total_requests']}")
        
        err_rate = (self.metrics['errors'] / self.metrics['total_requests']) * 100
        err_color = "green" if err_rate < 5 else "red"
        print(f"Error Rate:     {colored(f'{err_rate:.1f}%', err_color)}")
        
        lat_color = "green" if self.metrics['avg_latency_ms'] < 1000 else "yellow"
        print(f"Avg Latency:    {colored(f'{self.metrics['avg_latency_ms']} ms', lat_color)}")

        # 2. Quality Metrics (The "Glass Box")
        print(colored("\n🧠 Quality Metrics (Critic Evaluation)", "magenta", attrs=["bold"]))
        
        avg_score = sum(self.metrics['critic_scores']) / len(self.metrics['critic_scores'])
        hallucination_rate = len([s for s in self.metrics['critic_scores'] if s < 0.7]) / len(self.metrics['critic_scores']) * 100
        
        print(f"Avg Safety Score:      {avg_score:.2f} / 1.0")
        
        hal_color = "green" if hallucination_rate < 5 else "red"
        print(f"Hallucination Rate:    {colored(f'{hallucination_rate:.1f}%', hal_color)}")
        
        print("\n" + "="*50)
        if hallucination_rate > 5:
            print(colored("🚨 ALERT: High Hallucination Rate detected. Check Critic Logs.", "red", attrs=["bold", "blink"]))
        else:
            print(colored("✅ System Status: HEALTHY", "green", attrs=["bold"]))
        print("="*50)

if __name__ == "__main__":
    dashboard = QualityDashboard()
    dashboard.ingest_mock_data()
    dashboard.display()
