# 🎨 KisanAI - UI/UX Standardization Guide

> **Purpose:** Ensure consistent design patterns, components, and code style across the entire KisanAI application.

---

## 📦 New Reusable Components

We've created three new standardized components to replace inline form styling:

### 1. `Button.jsx` - Standardized Button Component

**Usage:**
```jsx
import Button from '../components/Button';

// Primary button
<Button variant="primary" onClick={handleClick}>
  Save Changes
</Button>

// With icon
<Button variant="primary" icon={Plus} onClick={handleAdd}>
  Add New
</Button>

// Loading state
<Button variant="primary" loading={isLoading}>
  Submitting...
</Button>

// Different sizes
<Button variant="primary" size="sm">Small</Button>
<Button variant="primary" size="md">Medium (default)</Button>
<Button variant="primary" size="lg">Large</Button>

// Variants
<Button variant="primary">Primary Action</Button>
<Button variant="secondary">Secondary Action</Button>
<Button variant="danger">Delete</Button>
<Button variant="outline">Cancel</Button>

// Full width
<Button variant="primary" fullWidth>Submit Form</Button>
```

**Props:**
- `variant`: `'primary' | 'secondary' | 'danger' | 'outline'` (default: `'primary'`)
- `size`: `'sm' | 'md' | 'lg'` (default: `'md'`)
- `loading`: `boolean` - Shows spinner and disables button
- `fullWidth`: `boolean` - Makes button full width
- `icon`: Lucide icon component
- `disabled`: `boolean`
- `type`: `'button' | 'submit' | 'reset'`

---

### 2. `Input.jsx` - Standardized Input Component

**Usage:**
```jsx
import Input from '../components/Input';

// Basic input
<Input
  label="Name"
  placeholder="Enter crop name"
  value={name}
  onChange={(e) => setName(e.target.value)}
/>

// Required field
<Input
  label="Email"
  type="email"
  required
  value={email}
  onChange={(e) => setEmail(e.target.value)}
/>

// With icon
<Input
  label="Search"
  placeholder="Search crops..."
  icon={Search}
  value={search}
  onChange={(e) => setSearch(e.target.value)}
/>

// With error
<Input
  label="Price"
  type="number"
  error="Price must be greater than 0"
  value={price}
  onChange={(e) => setPrice(e.target.value)}
/>
```

**Props:**
- `label`: `string` - Field label
- `error`: `string` - Error message
- `type`: `string` - HTML input type (default: `'text'`)
- `required`: `boolean` - Shows asterisk
- `placeholder`: `string`
- `icon`: Lucide icon component
- All standard HTML input props (`value`, `onChange`, `disabled`, etc.)

---

### 3. `Select.jsx` - Standardized Select Component

**Usage:**
```jsx
import Select from '../components/Select';

const cropOptions = [
  { value: 'wheat', label: 'Wheat' },
  { value: 'rice', label: 'Rice' },
  { value: 'corn', label: 'Corn' }
];

<Select
  label="Crop Type"
  required
  options={cropOptions}
  placeholder="Select a crop"
  value={selectedCrop}
  onChange={(e) => setSelectedCrop(e.target.value)}
/>

// With error
<Select
  label="State"
  options={stateOptions}
  error="Please select a state"
  value={state}
  onChange={(e) => setState(e.target.value)}
/>
```

**Props:**
- `label`: `string` - Field label
- `error`: `string` - Error message
- `required`: `boolean` - Shows asterisk
- `options`: `Array<{value: string, label: string}>` - Dropdown options
- `placeholder`: `string` - Placeholder text
- All standard HTML select props

---

## 🎨 Design Tokens

### Colors

```js
// Primary Palette
const colors = {
  primary: {
    DEFAULT: '#16a34a', // green-600
    hover: '#15803d',   // green-700
    light: '#22c55e',   // green-500
  },
  
  danger: {
    DEFAULT: '#dc2626', // red-600
    hover: '#b91c1c',   // red-700
    light: '#ef4444',   // red-500
  },
  
  info: {
    DEFAULT: '#2563eb', // blue-600
    hover: '#1d4ed8',   // blue-700
    light: '#3b82f6',   // blue-500
  },
  
  warning: {
    DEFAULT: '#ea580c', // orange-600
    hover: '#c2410c',   // orange-700
    light: '#f97316',   // orange-500
  },
  
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  }
};
```

**Usage in Tailwind:**
- Primary actions: `bg-green-600 hover:bg-green-700`
- Danger actions: `bg-red-600 hover:bg-red-700`
- Info cards: `bg-blue-50 border-blue-200`
- Text: `text-gray-900` (headings), `text-gray-700` (body), `text-gray-500` (secondary)

---

### Spacing System

**Use Tailwind's built-in scale consistently:**

```js
// Padding/Margin Scale (use these consistently)
const spacing = {
  xs: 'p-2',      // 8px  - Tight spacing
  sm: 'p-3',      // 12px - Compact elements
  md: 'p-4',      // 16px - Default cards
  lg: 'p-6',      // 24px - Large cards, modals
  xl: 'p-8',      // 32px - Page containers
};

// Gaps (for flex/grid)
const gaps = {
  xs: 'gap-2',    // 8px
  sm: 'gap-3',    // 12px
  md: 'gap-4',    // 16px - Most common
  lg: 'gap-6',    // 24px - Card grids
  xl: 'gap-8',    // 32px - Sections
};
```

**Examples:**
```jsx
// Card padding
<div className="bg-white rounded-lg shadow-md p-6">

// Grid layout
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

// Form spacing
<div className="space-y-4">
```

---

### Typography

```js
// Headings
const headings = {
  h1: 'text-3xl md:text-4xl font-bold text-gray-900',
  h2: 'text-2xl md:text-3xl font-bold text-gray-900',
  h3: 'text-xl md:text-2xl font-semibold text-gray-900',
  h4: 'text-lg md:text-xl font-semibold text-gray-800',
};

// Body text
const body = {
  large: 'text-lg text-gray-700',
  default: 'text-base text-gray-700',
  small: 'text-sm text-gray-600',
  tiny: 'text-xs text-gray-500',
};

// Labels
const labels = {
  default: 'text-sm font-medium text-gray-700',
  required: 'text-sm font-medium text-gray-700',
};
```

**Usage:**
```jsx
<h1 className="text-3xl md:text-4xl font-bold text-gray-900">Dashboard</h1>
<p className="text-base text-gray-700">Welcome back, farmer!</p>
<label className="text-sm font-medium text-gray-700">Crop Name</label>
```

---

### Shadows & Borders

```js
// Shadows
const shadows = {
  sm: 'shadow-sm',       // Subtle - inputs, buttons
  md: 'shadow-md',       // Default - cards
  lg: 'shadow-lg',       // Elevated - modals, dropdowns
  xl: 'shadow-xl',       // Prominent - hero cards
};

// Borders
const borders = {
  default: 'border-2 border-gray-300',
  focus: 'focus:border-green-500 focus:ring-2 focus:ring-green-500',
  error: 'border-red-300 focus:border-red-500',
};

// Rounded corners
const rounded = {
  sm: 'rounded',         // 4px
  md: 'rounded-lg',      // 8px - Default
  lg: 'rounded-xl',      // 12px - Large cards
  full: 'rounded-full',  // Pills, avatars
};
```

**Usage:**
```jsx
<div className="bg-white rounded-lg shadow-md border-2 border-gray-200">
<button className="rounded-lg shadow-sm hover:shadow-md">
```

---

## 🧩 Component Patterns

### Card Pattern

```jsx
// Standard card
<div className="bg-white rounded-lg shadow-md border-2 border-gray-200 p-6 hover:shadow-lg transition-shadow">
  <h3 className="text-xl font-semibold text-gray-900 mb-2">Card Title</h3>
  <p className="text-gray-600">Card description...</p>
</div>

// With icon header
<div className="bg-white rounded-lg shadow-md border-2 border-gray-200 p-6">
  <div className="flex items-center gap-3 mb-4">
    <div className="p-2 bg-green-100 rounded-lg">
      <Icon size={24} className="text-green-600" />
    </div>
    <h3 className="text-xl font-semibold text-gray-900">Title</h3>
  </div>
  <p className="text-gray-600">Content...</p>
</div>

// Colored card (for stats)
<div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-lg shadow-lg p-6">
  <h3 className="text-lg font-medium mb-1">Total Income</h3>
  <p className="text-3xl font-bold">₹45,200</p>
</div>
```

---

### Form Pattern

**Old (inconsistent):**
```jsx
<input
  type="text"
  placeholder="Name"
  className="w-full px-3 py-2 border rounded-lg"
  value={name}
  onChange={(e) => setName(e.target.value)}
/>
```

**New (standardized):**
```jsx
import Input from '../components/Input';
import Button from '../components/Button';

<form onSubmit={handleSubmit} className="space-y-4">
  <Input
    label="Crop Name"
    required
    placeholder="e.g., Wheat"
    value={name}
    onChange={(e) => setName(e.target.value)}
  />
  
  <Select
    label="Type"
    required
    options={cropTypes}
    value={type}
    onChange={(e) => setType(e.target.value)}
  />
  
  <div className="flex gap-3 justify-end">
    <Button variant="outline" onClick={onCancel}>
      Cancel
    </Button>
    <Button variant="primary" type="submit" loading={isSubmitting}>
      Submit
    </Button>
  </div>
</form>
```

---

### Modal Pattern

```jsx
<Modal isOpen={isOpen} onClose={onClose} title="Add New Item">
  <form onSubmit={handleSubmit} className="space-y-4">
    {/* Form fields using Input/Select components */}
    
    <div className="flex gap-3 justify-end pt-4 border-t">
      <Button variant="outline" onClick={onClose}>
        Cancel
      </Button>
      <Button variant="primary" type="submit" loading={isSubmitting}>
        Save
      </Button>
    </div>
  </form>
</Modal>
```

---

### List Pattern

```jsx
// Empty state
{items.length === 0 && (
  <EmptyState
    icon={Icon}
    title="No items found"
    description="Get started by adding your first item"
    actionLabel="Add Item"
    onAction={handleAdd}
  />
)}

// With items
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map((item, index) => (
    <motion.div
      key={item.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      <div className="bg-white rounded-lg shadow-md p-6">
        {/* Card content */}
      </div>
    </motion.div>
  ))}
</div>
```

---

### Loading Pattern

```jsx
import { SkeletonList } from '../components/SkeletonLoader';

{isLoading && <SkeletonList count={3} />}
{error && <p className="text-red-600">Error: {error.message}</p>}
{data && (
  <div className="grid gap-6">
    {/* Render data */}
  </div>
)}
```

---

## 🎯 Animation Guidelines

### Page Transitions

```jsx
import PageTransition from '../components/PageTransition';

export default function MyPage() {
  return (
    <PageTransition>
      {/* Page content */}
    </PageTransition>
  );
}
```

### List Animations

```jsx
import { motion } from 'framer-motion';

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.div variants={container} initial="hidden" animate="show" className="grid gap-6">
  {items.map((item) => (
    <motion.div key={item.id} variants={item}>
      <Card />
    </motion.div>
  ))}
</motion.div>
```

### Button Hover

```jsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  className="..."
>
  Click me
</motion.button>
```

---

## 📱 Responsive Design Rules

### Grid Layouts

```jsx
// 1 column on mobile, 2 on tablet, 3 on desktop
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">

// Always use responsive gaps
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
```

### Text Sizing

```jsx
// Headings should scale
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">

// Body text can stay fixed or scale slightly
<p className="text-sm md:text-base">
```

### Padding/Spacing

```jsx
// Cards: smaller padding on mobile
<div className="p-4 md:p-6">

// Containers: responsive padding
<div className="px-4 md:px-6 lg:px-8">
```

---

## ✅ Code Quality Checklist

### Before Submitting Code:

- [ ] Use `Button`, `Input`, `Select` components instead of inline styles
- [ ] Consistent color scheme (green for primary, red for danger)
- [ ] Consistent spacing (gap-4, gap-6, p-4, p-6)
- [ ] Responsive design (grid with md:, lg: breakpoints)
- [ ] Loading states with `SkeletonLoader`
- [ ] Empty states with `EmptyState` component
- [ ] Error handling with try/catch and error messages
- [ ] Animations with Framer Motion (optional but encouraged)
- [ ] Forms use `space-y-4` for field spacing
- [ ] Buttons use proper variants (primary, secondary, danger, outline)

---

## 🚫 Common Mistakes to Avoid

### ❌ Don't Do This:

```jsx
// Inline button with custom styles
<button className="bg-blue-500 px-4 py-2 rounded text-white" onClick={...}>
  Submit
</button>

// Inconsistent input styling
<input className="border p-2 rounded w-full" />

// No loading state
<button onClick={handleSubmit}>Save</button>

// No empty state
{items.length === 0 && <p>No items</p>}
```

### ✅ Do This Instead:

```jsx
import Button from '../components/Button';
import Input from '../components/Input';
import EmptyState from '../components/EmptyState';

// Standardized button
<Button variant="primary" onClick={handleClick}>
  Submit
</Button>

// Standardized input
<Input label="Name" value={name} onChange={...} />

// Loading state
<Button variant="primary" loading={isSubmitting} onClick={handleSubmit}>
  Save
</Button>

// Empty state
{items.length === 0 && (
  <EmptyState
    icon={Icon}
    title="No items found"
    description="Add your first item to get started"
  />
)}
```

---

## 📝 Migration Guide

### Step 1: Update Imports

```jsx
// Add these imports to your pages
import Button from '../components/Button';
import Input from '../components/Input';
import Select from '../components/Select';
```

### Step 2: Replace Buttons

**Find and replace:**
```jsx
// Old
<button className="bg-green-600 text-white px-4 py-2 rounded-lg" onClick={...}>
  Save
</button>

// New
<Button variant="primary" onClick={...}>
  Save
</Button>
```

### Step 3: Replace Inputs

**Find and replace:**
```jsx
// Old
<input
  type="text"
  placeholder="Name"
  className="w-full border-2 border-gray-300 px-3 py-2 rounded-lg"
  value={name}
  onChange={(e) => setName(e.target.value)}
/>

// New
<Input
  placeholder="Name"
  value={name}
  onChange={(e) => setName(e.target.value)}
/>
```

### Step 4: Replace Selects

**Find and replace:**
```jsx
// Old
<select className="w-full border-2 px-3 py-2 rounded-lg" value={...} onChange={...}>
  <option value="">Select...</option>
  <option value="1">Option 1</option>
</select>

// New
<Select
  options={[
    { value: '1', label: 'Option 1' }
  ]}
  value={...}
  onChange={...}
/>
```

---

## 🎉 Benefits of Standardization

1. **Consistency:** All buttons/inputs look the same
2. **Maintainability:** Change styling in one place
3. **Accessibility:** Components have proper focus/aria attributes
4. **Developer Experience:** Easier to write forms
5. **Performance:** Optimized animations and transitions
6. **Testing:** Easier to test standardized components

---

**Next Steps:**
1. ✅ Review this guide
2. 🔧 Gradually migrate existing pages to use new components
3. 🔧 Always use new components for new features
4. 📚 Update this guide as patterns evolve

---

**Guide Version:** 1.0  
**Last Updated:** November 20, 2025
