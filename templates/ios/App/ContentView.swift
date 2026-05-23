import SwiftUI

// Premium Glassmorphic Card View demonstrating the Monorepo Design Contract
struct ContentView: View {
    // State for micro-animations
    @State private var isHovered = false
    @State private var isPressed = false
    @State private var scale: CGFloat = 1.0
    
    // Brand design tokens
    let googleBrandGreen = Color(red: 0.204, green: 0.659, blue: 0.325) // #34A853
    let darkSlateBackground = Color(red: 0.043, green: 0.059, blue: 0.098) // #0B0F19 (HSL tailored slate)
    
    // Secure configuration mapped to environments populated by HashiCorp Vault
    let apiEndpoint = ProcessInfo.processInfo.environment["VAULT_API_ENDPOINT"] ?? "https://api.nebula.factory.internal"
    let storageBucket = ProcessInfo.processInfo.environment["VAULT_GCS_BUCKET_NAME"] ?? "factory-nebula-assets"
    
    var body: some View {
        ZStack {
            // Dark Slate background according to contract
            darkSlateBackground
                .ignoresSafeArea()
            
            VStack(spacing: 24) {
                // Header
                VStack(spacing: 8) {
                    Text("APP FACTORY")
                        .font(.custom("Outfit-Bold", size: 14))
                        .kerning(4)
                        .foregroundColor(googleBrandGreen)
                    
                    Text("Nebula Core")
                        .font(.custom("Outfit-Bold", size: 36))
                        .foregroundColor(.white)
                }
                .padding(.top, 40)
                
                Spacer()
                
                // Glassmorphic Card Container
                VStack(alignment: .leading, spacing: 20) {
                    HStack {
                        Image(systemName: "cpu.fill")
                            .font(.title)
                            .foregroundColor(googleBrandGreen)
                        Spacer()
                        Text("ACTIVE SECURE CONTEXT")
                            .font(.custom("Inter-Medium", size: 10))
                            .foregroundColor(.white.opacity(0.6))
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(googleBrandGreen.opacity(0.15))
                            .cornerRadius(4)
                    }
                    
                    Text("Secure OIDC Session Established")
                        .font(.custom("Outfit-SemiBold", size: 20))
                        .foregroundColor(.white)
                    
                    VStack(alignment: .leading, spacing: 12) {
                        InfoRow(title: "Vault Namespace", value: "secret/data/app-factory/app-01-nebula")
                        InfoRow(title: "Secure Host", value: apiEndpoint)
                        InfoRow(title: "GCS Bucket", value: storageBucket)
                    }
                    .padding(.top, 8)
                }
                .padding(24)
                .background(
                    RoundedRectangle(cornerRadius: 24)
                        .fill(Color.white.opacity(0.05))
                        .overlay(
                            RoundedRectangle(cornerRadius: 24)
                                .stroke(Color.white.opacity(0.1), lineWidth: 1)
                        )
                )
                .background(VisualEffectBlur(material: .hudWindow, blendingMode: .withinWindow)) // Glassmorphism backdrop blur
                .padding(.horizontal, 24)
                .scaleEffect(scale)
                .animation(.spring(response: 0.4, dampingFraction: 0.75, blendDuration: 0), value: scale)
                
                Spacer()
                
                // Action Button with micro-animations
                Button(action: {
                    withAnimation(.easeInOut(duration: 0.1)) {
                        self.scale = 0.97
                    }
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                        withAnimation(.spring(response: 0.4, dampingFraction: 0.6)) {
                            self.scale = 1.0
                        }
                    }
                }) {
                    Text("Sync Infrastructure")
                        .font(.custom("Inter-SemiBold", size: 16))
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 56)
                        .background(googleBrandGreen)
                        .cornerRadius(16)
                        .shadow(color: googleBrandGreen.opacity(0.3), radius: 12, x: 0, y: 6)
                }
                .padding(.horizontal, 24)
                .padding(.bottom, 40)
            }
        }
    }
}

struct InfoRow: View {
    let title: String
    let value: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.custom("Inter-Regular", size: 12))
                .foregroundColor(.white.opacity(0.5))
            Text(value)
                .font(.custom("Inter-Medium", size: 14))
                .foregroundColor(.white.opacity(0.9))
                .lineLimit(1)
        }
    }
}

// Visual Effect Blur helper for macOS/iOS Glassmorphism
struct VisualEffectBlur: UIViewRepresentable {
    var material: UIBlurEffect.Style
    var blendingMode: UIVisualEffectView.BlendingMode = .withinWindow
    
    func makeUIView(context: Context) -> UIVisualEffectView {
        let view = UIVisualEffectView(effect: UIBlurEffect(style: material))
        return view
    }
    
    func updateUIView(_ uiView: UIVisualEffectView, context: Context) {
        uiView.effect = UIBlurEffect(style: material)
    }
}

#Preview {
    ContentView()
}
