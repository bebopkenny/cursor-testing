# SDSU Student Experience Dashboard

A modern Next.js application for visualizing San Diego State University student living experiences, mental health, and campus community data. This interactive dashboard helps students provide feedback and allows administrators to understand student needs through data-driven insights.

## 🌟 Features

- **Interactive Survey Interface**: Clean, user-friendly numeric input components with validation
- **Real-time Data Visualization**: Dynamic charts using Chart.js showing response distributions
- **Responsive Design**: Fully optimized for desktop, tablet, and mobile devices
- **Modern UI/UX**: Built with Tailwind CSS for a professional, accessible interface
- **Type Safety**: Full TypeScript implementation for robust development
- **Mock Authentication**: OAuth 2.0 style login with Google and SDSU account options

## 📊 Survey Categories

The dashboard collects and visualizes data across five key areas:

1. **Mental Health Rating** - Overall mental health and well-being assessment
2. **Counseling Services Usage** - Frequency of campus mental health resource utilization
3. **Conflict Avoidance** - Tendency to avoid interpersonal conflicts in living situations
4. **Sense of Belonging** - Connection and integration within the university environment
5. **Room Switch Requests** - Likelihood of requesting housing changes

## 🛠️ Tech Stack

- **Frontend Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Chart.js with react-chartjs-2
- **Icons**: Heroicons (SVG)
- **Font**: Inter (Google Fonts)

## 🚀 Getting Started

### Prerequisites

- Node.js 18.x or later
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sdsu-student-dashboard
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## 📱 Responsive Design

The application is fully responsive with Tailwind CSS breakpoints:

- **Mobile**: `< 640px` - Single column layout, simplified navigation
- **Tablet**: `640px - 1024px` - Two-column layouts where appropriate
- **Desktop**: `> 1024px` - Full multi-column layouts, expanded visualizations

### Key Responsive Features

- Collapsible navigation elements on mobile
- Responsive chart sizing and legend positioning
- Touch-friendly input controls
- Optimized text sizing and spacing

## 🎨 Design System

### Color Palette

- **Primary**: Blue gradient (`from-blue-600 to-purple-600`)
- **Success**: Green (`#10B981`)
- **Warning**: Yellow (`#F59E0B`) 
- **Error**: Red (`#EF4444`)
- **Neutral**: Gray scale for text and backgrounds

### Typography

- **Font Family**: Inter (system fallback: sans-serif)
- **Headings**: Bold weights (600-700)
- **Body**: Regular weight (400)
- **Small Text**: Light weight (300-400)

## 📊 Data Visualization

### Chart Types

- **Pie Charts**: Primary visualization for survey response distribution
- **Bar Charts**: Alternative view for categorical data
- **Doughnut Charts**: Variant for compact displays

### Chart Features

- Interactive tooltips with detailed information
- Responsive sizing based on container
- Color-coded legends with accessibility considerations
- Smooth animations and transitions

## 🔐 Authentication (Demo)

The current implementation includes mock authentication for demonstration purposes:

- **Email/Password**: Standard form with validation
- **Google OAuth**: Simulated OAuth 2.0 flow
- **SDSU Account**: University-specific authentication option

*Note: All authentication methods redirect to the dashboard after a simulated delay.*

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── login/             # Login page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Dashboard (home)
│   └── globals.css        # Global styles
├── components/            # Reusable React components
│   ├── ChartConfig.ts     # Chart.js configuration
│   ├── NumericInput.tsx   # Survey input component
│   └── SurveyChart.tsx    # Chart visualization component
├── types/                 # TypeScript definitions
│   └── index.ts          # Interface definitions
└── utils/                 # Utility functions
    └── surveyUtils.ts     # Data processing functions
```

## 🎯 Future Enhancements

### Backend Integration
- Real authentication with university SSO
- Database integration for persistent data
- RESTful API for survey responses
- Administrative dashboard for data analysis

### Additional Features
- Export functionality (PDF, CSV)
- Comparative analytics across time periods
- Advanced filtering and segmentation
- Email notifications and reporting

### Accessibility Improvements
- ARIA labels and roles
- Keyboard navigation optimization
- Screen reader compatibility
- High contrast mode support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is created for San Diego State University and is intended for educational and administrative purposes.

## 📞 Support

For questions or support regarding this dashboard, please contact:
- SDSU Student Services
- IT Support
- Student Affairs Office

---

**Built with ❤️ for SDSU Students**
