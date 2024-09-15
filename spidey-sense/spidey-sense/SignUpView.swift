import SwiftUI
import ClerkSDK

struct SignUpView: View {
  @State private var email = ""
  @State private var password = ""
  @State private var code = ""
  @State private var isVerifying = false
  
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
          Task { await signUp(email: email, password: password) }
        }
        .foregroundColor(Color.black)
      }
    }
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

      isVerifying = true
    } catch {
      dump(error)
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
      dump(error)
    }
  }
  
}
