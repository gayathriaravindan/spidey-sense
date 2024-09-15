//
//  MainTab.swift
//  spidey-sense
//
//  Created by Nandini Bhatt on 9/15/24.
//
import SwiftUI

struct MainView: View {
    @State private var selectedTab = 1

    var body: some View {
        TabView(selection: $selectedTab) {
            // Activity Tab
            NavigationView {
                ActivityTrackingView()
            }
            .tabItem {
                Label("Activity", systemImage: "waveform.path.ecg")
            }
            .tag(1)
            
            // Profile Tab
            NavigationView {
                ProfileView()
            }
            .tabItem {
                Label("Profile", systemImage: "person.circle")
            }
            .tag(2)
        }
    }
}

struct MainView_Previews: PreviewProvider {
    static var previews: some View {
        MainView()
    }
}
