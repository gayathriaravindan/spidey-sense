//
//  WelcomeView.swift
//  MiTHack
//
//  Created by Gayathri Aravindan on 9/15/24.
//

import ClerkSDK
import SwiftUI

struct WelcomeView: View {
    
    @ObservedObject private var clerk = Clerk.shared
    
    var body: some View {
        ZStack {
            Color(hex: "#FFFFFF")
                .ignoresSafeArea()

            VStack {
                Image("spider-sense-logo")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 150, height: 150)
                    .padding(.top, 50)
                    .padding(.bottom, 5)

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
}


struct SignUpOrSignInView: View {
  @State private var isSignUp = true
  
  var body: some View {
    ScrollView {
      if isSignUp {
        SignUpView()
      } else {
        SignInView()
      }
      
      Button {
        isSignUp.toggle()
      } label: {
        if isSignUp {
          Text("Already have an account? Sign In")
                .foregroundColor(Color.black)
        } else {
          Text("Don't have an account? Sign Up")
                .foregroundColor(Color.black)
        }
      }
      .padding()
    }
  }
}


struct SignUpView: View {
    @State private var email = ""
    @State private var password = ""
    @State private var code = ""
    @State private var isVerifying = false
    @State private var showMainTab = false
    @State private var showError = false
    @State private var errorMessage: String?
  
  var body: some View {
    VStack {
      Text("Spidey Sense")
            .font(.largeTitle)
            .fontWeight(.bold)
            .foregroundColor(Color(hex: "#b11313"))
            .padding(.bottom, 20)
        
        Text("Sign Up")
              .font(.title3)
              .fontWeight(.bold)
              .foregroundColor(Color(hex: "#000000"))

      if isVerifying {
        TextField("Code", text: $code)
        Button("Verify") {
          Task { await verify(code: code) }
        }
      } else {
        TextField("Email", text: $email)
              .background(Color.white)
        SecureField("Password", text: $password)
              .background(Color.white)
              .padding(.bottom, 20)
        Button("Continue") {
          Task { 
              await signUp(email: email, password: password)
          }
        }
        .foregroundColor(Color.black)
      }
    }
    .fullScreenCover(isPresented: $showMainTab, content: {
        MainView()
    })
    .alert("Error. Try New Password.", isPresented: $showError, actions: {
        Button("Got It", role: .cancel, action: {})
    })
    .padding()
  }
}

extension SignUpView {
  
  func signUp(email: String, password: String) async {
    do {
        let signUp = try await SignUp.create(
            strategy: .standard(emailAddress: email, password: password)
        )
                
        try await signUp.prepareVerification(strategy: .emailCode)
        
        showMainTab = true

        isVerifying = true
    } catch {
        dump(error)
        errorMessage = (error as? ClerkAPIError)?.errorDescription ?? error.localizedDescription
        showError = true
    }
  }
  
  func verify(code: String) async {
    do {
        guard let signUp = await Clerk.shared.client?.signUp else {
        isVerifying = false
        return
      }
      
      try await signUp.attemptVerification(.emailCode(code: code))
    } catch {
        errorMessage = error.localizedDescription
        showError = true
      dump(error)
    }
  }
  
}


struct SignInView: View {
    @State private var email = ""
    @State private var password = ""
    @State private var showMainTab = false
    @State private var showError = false
    @State private var errorMessage: String?
  
  var body: some View {
    VStack {
        Text("Spidey Sense")
              .font(.largeTitle)
              .fontWeight(.bold)
              .foregroundColor(Color(hex: "#b11313"))
              .padding(.bottom, 20)
          
          Text("Sign In")
                .font(.title3)
                .fontWeight(.bold)
                .foregroundColor(Color(hex: "#000000"))
      TextField("Email", text: $email)
            .background(Color.white)
      SecureField("Password", text: $password)
            .background(Color.white)
            .padding(.bottom, 20)
      Button("Continue") {
        Task { 
            await submit(email: email, password: password)
        }
      }
      .foregroundColor(Color.black)
    }
    .padding()
    .fullScreenCover(isPresented: $showMainTab, content: {
        MainView()
    })
    .alert("Failed to sing up with error", isPresented: $showError, actions: {
        Button("Got It", role: .cancel, action: {})
    })
  }
}

extension SignInView {
    
  func submit(email: String, password: String) async {
    do {
        try await SignIn.create(
            strategy: .identifier(email, password: password)
        )
        
        let token = try await Clerk.shared.session?.getToken()?.jwt
        print("Token: ", token ?? "Unknown token")
        
        
        HTTPRequestClient.Builder()
            .setMethod(.POST)
            .setUrl("localhost:8081")
            .withInput(TokenReponse.self)
            .setHeaders(
                [
                    "Authorization": "Bearer \(token ?? "Unknown token")",
                ]
            )
            .build()
            .executeAndGetResult { response in
                print(">>>response: ", response)
            }
        
        showMainTab = true
    } catch {
        dump(error)
        errorMessage = error.localizedDescription
        showError = true
    }
  }
    
}
