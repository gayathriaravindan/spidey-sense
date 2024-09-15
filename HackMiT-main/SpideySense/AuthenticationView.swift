//
//  AuthenticationView.swift
//  MiTHack
//
//  Created by Gayathri Aravindan on 9/15/24.
//

import SwiftData
import ClerkSDK
import SwiftUI

struct AuthenticationView: View {
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

    var body: some View {
        Group {
            ZStack {
                if clerk.loadingState == .notLoaded {
                    SplashScreenView()
                } else {
                    WelcomeView()
                }
            }
            .task {
                clerk.configure(publishableKey: "pk_test_cmljaC1oeWVuYS04OC5jbGVyay5hY2NvdW50cy5kZXYk")
                try? await clerk.load()
            }
        }
        .modelContainer(sharedModelContainer)
    }
}


#Preview {
    AuthenticationView()
}
