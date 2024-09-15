//
//  ProfileView.swift
//  SpideySense
//
//  Created by Gayathri Aravindan on 9/15/24.
//

import SwiftUI

struct ProfileView: View {
    @State private var sensitivity: Float = 5.0
    @State private var timerLength: Int = 10
    @State private var alarmNoise: String = "Loud"
    @State private var callCops: Bool = false
    @State private var emergencyContacts: [String] = ["Mom: (123)-456-7890"]

    let alarmOptions = ["Silent", "Loud"]
    
    var body: some View {
        VStack {
            HStack {
                Text("Profile Settings")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                
                Spacer()
                
                // Settings Button
                NavigationLink(destination: SettingsView()) {
                    Image(systemName: "gear")
                        .font(.title2)
                }
            }
            .padding(.horizontal)
            .padding(.top, 30)

            Form {
                // Sensitivity
                Section(header: Text("Sensitivity")) {
                    VStack(alignment: .leading) {
                        Text("Sensitivity Level: \(String(format: "%.1f", sensitivity))")
                        Slider(value: $sensitivity, in: 1...10, step: 0.1)
                    }
                }
                
                // Countdown Timer Length
                Section(header: Text("Countdown Timer Length")) {
                    Stepper(value: $timerLength, in: 1...60) {
                        Text("\(timerLength) seconds")
                    }
                }
                
                // Alarm Noise
                Section(header: Text("Alarm Noise")) {
                    Picker("Select Alarm Noise", selection: $alarmNoise) {
                        ForEach(alarmOptions, id: \.self) { option in
                            Text(option).tag(option)
                        }
                    }
                    .pickerStyle(SegmentedPickerStyle())
                }
                
                // Call Cops
                Section(header: Text("Call Cops")) {
                    Toggle(isOn: $callCops) {
                        Text("Call cops if danger detected")
                    }
                }
                
                // Emergency Contacts
                Section(header: Text("Emergency Contacts")) {
                    List {
                        ForEach(emergencyContacts, id: \.self) { contact in
                            Text(contact)
                        }
                        .onDelete(perform: deleteContact)
                        
                        Button(action: addContact) {
                            Text("Add Contact")
                        }
                    }
                }
            }
        }
        .navigationBarHidden(true)
    }
    
    // Add Contact (dummy implementation)
    func addContact() {
        emergencyContacts.append("New Contact")
    }
    
    // Delete Contact
    func deleteContact(at offsets: IndexSet) {
        emergencyContacts.remove(atOffsets: offsets)
    }
}

// Settings View
struct SettingsView: View {
    var body: some View {
        VStack {
            Text("Settings")
                .font(.largeTitle)
                .padding()
            Spacer()
        }
    }
}

struct ProfileView_Previews: PreviewProvider {
    static var previews: some View {
        ProfileView()
    }
}
