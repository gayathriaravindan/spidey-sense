//
//  Activity.swift
//  spidey-sense
//
//  Created by Nandini Bhatt on 9/15/24.
//

import SwiftUI
import Charts

struct ActivityTrackingView: View {
    // Mock Data for graph (Weekly)
    let weeklyData: [ActivityData] = [
        ActivityData(day: "Mon", heartRate: 105, abnormal: true),
        ActivityData(day: "Tue", heartRate: 95, abnormal: false),
        ActivityData(day: "Wed", heartRate: 110, abnormal: true),
        ActivityData(day: "Thu", heartRate: 85, abnormal: false),
        ActivityData(day: "Fri", heartRate: 100, abnormal: false),
        ActivityData(day: "Sat", heartRate: 115, abnormal: true),
        ActivityData(day: "Sun", heartRate: 90, abnormal: false)
    ]
    
    // Example recent calls (with time and contacts)
    @State private var recentCalls: [String] = [
        "Mom - 6:34 PM, Today 9/15",
        "Police - 3:30 PM, Thursday 9/12 ",
        "Dad - 1:22 AM, Monday 7/1"
    ]
    
    var body: some View {
        NavigationView {
            TabView {
                // Activity Tab
                VStack {
                    // Header
                    HStack {
                        Text("Activity")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .padding(.top, 30)
                        
                        Spacer()
                        
                        // Settings Button
                        NavigationLink(destination: SettingsView()) {
                            Image(systemName: "gear")
                                .font(.title2)
                                .padding(.top, 30)
                        }
                    }
                    .padding(.horizontal)

                    ScrollView {
                        VStack(alignment: .leading, spacing: 15) {
                            
                            // Weekly Graph for Abnormal Activity
                            VStack {
                                Text("Weekly Fear/Stress Tracking")
                                    .font(.headline)
                                
                                Chart {
                                    ForEach(weeklyData, id: \.day) { data in
                                        LineMark(
                                            x: .value("Day", data.day),
                                            y: .value("Heart Rate", data.heartRate)
                                        )
                                        .foregroundStyle(data.abnormal ? .red : .blue)
                                    }
                                }
                                .frame(height: 200)
                                .padding()
                            }
                            .background(RoundedRectangle(cornerRadius: 10).fill(Color(.systemGray6)))
                            
                            // Recent Calls Section
                            VStack(alignment: .leading, spacing: 15) {
                                Text("Recent Calls")
                                    .font(.headline)
                                
                                // Show recent calls as a list
                                ForEach(recentCalls, id: \.self) { call in
                                    Text(call)
                                        .padding()
                                        .foregroundColor(Color.white)
                                        .background(RoundedRectangle(cornerRadius: 5).fill(Color.red))
                                }
                            }
                            .padding()
                            .background(RoundedRectangle(cornerRadius: 10).fill(Color(.systemGray6)))
                        }
                        .padding()
                    }
                }
                .tabItem {
                    Label("Activity", systemImage: "waveform.path.ecg")
                }
                
                // Docs Tab (Placeholder)
                VStack {
                    Text("Docs Section")
                        .font(.largeTitle)
                        .padding()
                }
                .tabItem {
                    Label("Docs", systemImage: "doc.text")
                }
                
                // Profile Tab (Placeholder)
                VStack {
                    Text("Profile Section")
                        .font(.largeTitle)
                        .padding()
                }
                .tabItem {
                    Label("Profile", systemImage: "person.circle")
                }
            }
        }
    }
}

// Settings View
//struct SettingsView: View {
//    var body: some View {
//        Text("Settings")
//            .font(.largeTitle)
//            .padding()
//    }
//}

// Data Model for Weekly Activity Data
struct ActivityData: Identifiable {
    let id = UUID()
    let day: String
    let heartRate: Int
    let abnormal: Bool
}

struct ActivityTrackingView_Previews: PreviewProvider {
    static var previews: some View {
        ActivityTrackingView()
    }
}
