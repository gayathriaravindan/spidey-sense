//
//  ContentView.swift
//  spidey-sense
//
//  Created by Gayathri Aravindan on 9/14/24.
//

import SwiftUI
import ClerkSDK

struct ContentView: View {
    @ObservedObject private var clerk = Clerk.shared
    var body: some View {
        VStack {
              if let user = clerk.user {
                Text("Hello, \(user.id)")
                  Button("Sign Out") {
                            Task { try? await clerk.signOut() }
                          }
              } else {
                  SignUpOrSignInView()
              }
        }
    }
}

#Preview {
    ContentView()
}
