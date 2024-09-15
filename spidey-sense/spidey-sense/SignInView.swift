import SwiftUI
import ClerkSDK

struct SignInView: View {
  @State private var email = ""
  @State private var password = ""
  
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
        Task { await submit(email: email, password: password) }
      }
      .foregroundColor(Color.black)
    }
    .padding()
  }
}

extension SignInView {
    
  func submit(email: String, password: String) async {
    do {
      try await SignIn.create(
        strategy: .identifier(email, password: password)
      )
    } catch {
      dump(error)
    }
  }
    
}
