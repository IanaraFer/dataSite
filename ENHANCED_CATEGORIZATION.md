# Enhanced Financial Categorization System

## Overview
The Financial Diagnosis module now includes **intelligent automatic categorization** that identifies and tracks all major spending categories in Portuguese and English bank statements.

---

## 🎯 Categories Automatically Identified

### 1. **Shopping** (Supermercados/Compras)
Identifies:
- Lidl, Aldi, Continente, Pingo Doce, Intermarché, Minipreço
- Jumbo, Auchan, El Corte Inglés
- Any grocery/supermarket transactions

### 2. **Pharmacies** (Farmácias)
Identifies:
- Farmácia, Pharmacy, Wells
- Drug stores, medicine purchases
- Health products

### 3. **Morgadi** (Cafés/Pastelarias)
Identifies:
- Morgadi, Morgadinho
- Coffee shops, cafeterias
- Bakeries, snack bars

### 4. **Rent** (Renda/Aluguer)
Identifies:
- Rent, Renda, Aluguer, Arrendamento
- Landlord payments
- Housing/lease payments

### 5. **School** (Escola/Educação)
Identifies:
- Escola, School, University, Faculdade
- Tuition fees (Propinas)
- School books and materials
- Education-related expenses

### 6. **Creches** (Infantário/Daycare)
Identifies:
- Creche, Jardim de Infância, Infantário
- Daycare, Nursery, Pre-school
- Childcare services

### 7. **Savings** (Poupança)
Identifies:
- Savings transfers
- Deposits to savings accounts
- Applications/investments in savings products

### 8. **Investment** (Investimento)
Identifies:
- Stock purchases (Ações)
- ETFs, Funds, Crypto
- Trading platforms (Degiro, Revolut)
- Investment applications

### 9. **Insurance** (Seguros)
Identifies:
- Life, Health, Auto insurance
- Insurance companies: Tranquilidade, Fidelidade, Allianz, etc.
- Premium payments (Prémios)
- Policy payments

### 10. **Loans** (Empréstimos/Créditos)
Identifies:
- Loan payments (Empréstimos)
- Credit installments (Prestações)
- Bank financing
- Debt payments

### 11. **Utilities** (Serviços)
Identifies:
- Water (Água), Electricity (Luz), Gas (Gás)
- EDP, Galp, EPAL
- Internet/Phone: NOS, MEO, Vodafone
- Telecommunications

### 12. **Transport** (Transportes)
Identifies:
- Fuel: Gasolina, Diesel, Combustível
- Gas stations: Galp, BP, Repsol, Cepsa
- Public transport: Carris, Metro, Comboio
- Taxi, Uber, Bolt
- Tolls (Portagens), Parking

### 13. **Restaurants** (Restaurantes)
Identifies:
- Restaurants, cafes
- Fast food: McDonald's, Burger King, KFC
- Food delivery: Uber Eats, Glovo
- Dining out expenses

### 14. **Entertainment** (Entretenimento)
Identifies:
- Cinema, Theatre, Concerts, Festivals
- Streaming: Netflix, Spotify, Amazon Prime, Disney+
- Gym, Fitness, Sports
- Leisure activities

### 15. **Clothing** (Roupa)
Identifies:
- Clothing stores: Zara, H&M, Mango, Pull&Bear
- Shoes (Sapatos, Calçado)
- Fashion retailers

### 16. **Health** (Saúde)
Identifies:
- Hospital, Clinic visits
- Doctor appointments (Médico)
- Dentist (Dentista)
- Medical exams and tests

### 17. **Home** (Casa)
Identifies:
- Furniture (Mobília)
- IKEA, Leroy Merlin, AKI
- Home appliances (Electrodomésticos)
- Home decoration

### 18. **Taxes** (Impostos)
Identifies:
- IRS, IMI, IUC
- Tax payments
- Social Security (Segurança Social)
- Government fees

### 19. **Income** (Rendimentos)
Identifies:
- Salary (Salário, Vencimento)
- Wages, Bonuses
- Commission payments
- Allowances (Subsídios)

---

## 📊 Analysis Output

For each category, the system provides:

### **Per Category:**
- **Total Amount**: Sum of all transactions
- **Count**: Number of transactions
- **Average**: Average transaction amount
- **Percentage**: % of total expenses

### **Example Output:**
```json
{
  "Shopping": {
    "total": 450.25,
    "count": 15,
    "average": 30.02,
    "percentage": 18.5
  },
  "Rent": {
    "total": 800.00,
    "count": 1,
    "average": 800.00,
    "percentage": 32.9
  },
  "Pharmacies": {
    "total": 85.50,
    "count": 4,
    "average": 21.38,
    "percentage": 3.5
  }
}
```

---

## 🔍 How It Works

### **1. Keyword Matching**
- Scans transaction descriptions for category-specific keywords
- Supports both Portuguese and English terms
- Case-insensitive matching

### **2. Pattern Recognition**
- Uses regex patterns for flexible matching
- Identifies merchant names and transaction types
- Handles variations in naming

### **3. Smart Categorization**
- Preserves existing categories if already labeled
- Only categorizes uncategorized transactions
- Prioritizes most specific matches

---

## 💡 Usage Examples

### **API Call:**
```python
# Transactions are automatically categorized
analysis = analyze_finances(transactions_df, accounts_df)

# Access category breakdown
category_breakdown = analysis['expense_by_category']
# Returns: {'Shopping': {...}, 'Rent': {...}, ...}

# Get top spending categories
top_categories = analysis['top_spending_categories']
# Returns: [{'category': 'Rent', 'amount': 800, 'percentage': 32.9}, ...]
```

### **Frontend Display:**
The enhanced UI automatically shows:
- Category name
- Total amount spent
- Percentage of total expenses
- Number of transactions
- Visual progress bars

---

## 🎨 Frontend Features

### **Detailed Category Table**
Shows all identified categories with:
- Category name
- Total amount (€)
- Percentage (%)
- Transaction count
- Visual progress bar

### **Category Highlights**
Displays comprehensive list:
> 📊 **Categories Identified:** Shopping, Pharmacies, Morgadi, Rent, School, Creches, Savings, Investment, Insurance, Loans, Utilities, Transport, Restaurants, Entertainment, Clothing, Health, Home, Taxes, and more!

---

## 🔧 Technical Details

### **Files:**
- `categorizer.py` - Main categorization engine
- `analytics.py` - Integration with analysis pipeline
- `financial-diagnosis.html` - Enhanced UI display

### **Classes:**
- `PortugueseTransactionCategorizer` - Main categorization class
- Methods:
  - `categorize_transaction()` - Single transaction
  - `categorize_dataframe()` - Batch processing
  - `analyze_spending_by_category()` - Generate analysis
  - `get_category_breakdown_report()` - Text report

---

## 📈 Benefits

✅ **Automatic**: No manual categorization needed
✅ **Comprehensive**: 19+ categories identified
✅ **Bilingual**: Portuguese and English support
✅ **Accurate**: Intelligent pattern matching
✅ **Detailed**: Amount, count, percentage, average per category
✅ **Visual**: Beautiful charts and tables
✅ **Actionable**: Clear spending insights

---

## 🚀 Getting Started

1. Upload your bank statement (CSV, Excel, PDF)
2. System automatically categorizes all transactions
3. View detailed breakdown by category
4. See amounts, percentages, and trends
5. Get recommendations based on spending patterns

---

## 📝 Example Transaction Categorization

| Description | Category |
|------------|----------|
| "CONTINENTE SUPERMERCADO" | Shopping |
| "FARMACIA CENTRAL" | Pharmacies |
| "MORGADI CAFE" | Morgadi |
| "PAGAMENTO RENDA OUTUBRO" | Rent |
| "ESCOLA BASICA - PROPINAS" | School |
| "CRECHE LITTLE ANGELS" | Creches |
| "TRANSFER POUPANCA" | Savings |
| "DEGIRO - COMPRA ACOES" | Investment |
| "FIDELIDADE SEGURO AUTO" | Insurance |
| "PRESTACAO CREDITO HABITACAO" | Loans |
| "EDP - CONTA LUZ" | Utilities |
| "GALP COMBUSTIVEL" | Transport |
| "RESTAURANTE DONA MARIA" | Restaurants |

---

## 🎯 Next Enhancements

Planned improvements:
- Machine learning for better categorization
- Custom category rules
- Merchant name database
- Sub-category detection
- Multi-currency support

---

**Built with ❤️ for Analytica Core AI**
*Smart Financial Categorization for SMEs and Individuals*
