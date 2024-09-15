//
//  spidey_senseApp.swift
//  spidey-sense
//
//  Created by Gayathri Aravindan on 9/14/24.
//

import SwiftUI
import SwiftData
import ClerkSDK

@main
struct spidey_senseApp: App {
    @ObservedObject private var clerk = Clerk.shared
    @State private var showSplash = true
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            Item.self,
        ])
        let modelConfiguration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()

    var body: some Scene {
        WindowGroup {
            ZStack {
                if clerk.loadingState == .notLoaded {
                    ProgressView()
                } else {
                    ContentView()
                }
            }
            .task {
                clerk.configure(publishableKey: "YOUR_PUBLISHABLE_KEY")
                try? await clerk.load()
            }
        }
        .modelContainer(sharedModelContainer)
    }
}
