"""
Enhanced Transaction Categorization for Portuguese Financial Statements
Identifies specific spending categories: Shopping, Pharmacies, Morgadi, Rent, 
School, Creches, Savings, Investment, Insurance, Loans, etc.
"""

import pandas as pd
import re
from typing import Dict, List, Tuple


class PortugueseTransactionCategorizer:
    """
    Intelligent categorization system for Portuguese financial transactions
    """
    
    # Category mappings with keywords (Portuguese and English)
    CATEGORY_KEYWORDS = {
        'Shopping': [
            'lidl', 'aldi', 'continente', 'pingo doce', 'intermarche', 'minipreço',
            'jumbo', 'auchan', 'el corte', 'shopping', 'supermercado', 'mercado',
            'grocery', 'groceries', 'supermarket', 'market'
        ],
        'Pharmacies': [
            'farmacia', 'farmácia', 'pharmacy', 'wells', 'saude', 'saúde',
            'droga', 'medicamentos', 'medicines', 'drugstore'
        ],
        'Morgadi': [
            'morgadi', 'morgadinho', 'coffee', 'café', 'cafe', 'pastelaria',
            'cafeteria', 'padaria', 'bakery', 'snack'
        ],
        'Rent': [
            'renda', 'rent', 'aluguer', 'arrendamento', 'landlord', 'senhorio',
            'housing', 'habitação', 'lease'
        ],
        'School': [
            'escola', 'school', 'universidade', 'university', 'faculdade',
            'college', 'educação', 'education', 'propinas', 'tuition',
            'livros escolares', 'textbooks', 'material escolar'
        ],
        'Creches': [
            'creche', 'jardim de infância', 'infantário', 'daycare',
            'childcare', 'nursery', 'pre-school', 'pré-escola'
        ],
        'Savings': [
            'poupança', 'poupanca', 'savings', 'deposito', 'depósito',
            'aplicação', 'application', 'conta poupança', 'saving account',
            'transfer to savings', 'transferencia poupanca'
        ],
        'Investment': [
            'investimento', 'investment', 'ações', 'acoes', 'stocks', 'shares',
            'fundos', 'funds', 'etf', 'crypto', 'bitcoin', 'trading',
            'bolsa', 'stock market', 'degiro', 'revolut trading'
        ],
        'Insurance': [
            'seguro', 'insurance', 'seguradora', 'tranquilidade', 'fidelidade',
            'allianz', 'liberty', 'zurich', 'axa', 'premium', 'prémio',
            'apólice', 'policy', 'vida', 'life insurance', 'saúde insurance',
            'auto insurance', 'carro seguro'
        ],
        'Loans': [
            'emprestimo', 'empréstimo', 'loan', 'credito', 'crédito',
            'prestação', 'prestacao', 'payment', 'financiamento',
            'financing', 'debt', 'divida', 'dívida', 'banco', 'bank loan'
        ],
        'Utilities': [
            'agua', 'água', 'water', 'luz', 'electricidade', 'electricity',
            'gas', 'gás', 'edp', 'galp', 'epal', 'utilities', 'serviços',
            'services', 'internet', 'nos', 'meo', 'vodafone', 'telecomunicações'
        ],
        'Transport': [
            'combustivel', 'combustível', 'fuel', 'gasolina', 'gasoline',
            'diesel', 'galp', 'bp', 'repsol', 'cepsa', 'carris', 'metro',
            'comboio', 'train', 'autocarro', 'bus', 'taxi', 'uber', 'bolt',
            'via verde', 'portagem', 'toll', 'estacionamento', 'parking'
        ],
        'Restaurants': [
            'restaurante', 'restaurant', 'comida', 'food', 'refeição',
            'jantar', 'dinner', 'almoço', 'lunch', 'pequeno almoço',
            'breakfast', 'mcdonald', 'burger king', 'kfc', 'pizza hut',
            'uber eats', 'glovo', 'takeaway'
        ],
        'Entertainment': [
            'cinema', 'teatro', 'theatre', 'concerto', 'concert', 'festival',
            'netflix', 'spotify', 'amazon prime', 'disney', 'hbo',
            'entretenimento', 'entertainment', 'diversão', 'lazer',
            'ginasio', 'gym', 'fitness', 'desporto', 'sport'
        ],
        'Clothing': [
            'roupa', 'clothing', 'clothes', 'zara', 'h&m', 'mango',
            'pull&bear', 'bershka', 'stradivarius', 'sapatos', 'shoes',
            'calçado', 'footwear', 'fashion', 'moda'
        ],
        'Health': [
            'hospital', 'clinica', 'clínica', 'clinic', 'médico', 'medico',
            'doctor', 'dentista', 'dentist', 'consulta', 'appointment',
            'exame', 'exam', 'analises', 'análises', 'tests', 'lab'
        ],
        'Home': [
            'mobilia', 'mobília', 'furniture', 'ikea', 'decoração',
            'decoration', 'casa', 'home', 'bricolage', 'diy', 'leroy merlin',
            'aki', 'worten', 'electrodomésticos', 'appliances'
        ],
        'Taxes': [
            'irs', 'imi', 'iuc', 'taxa', 'tax', 'imposto', 'finanças',
            'finances', 'autoridade tributária', 'segurança social',
            'social security', 'tsu'
        ],
        'Income': [
            'salario', 'salário', 'salary', 'vencimento', 'wage', 'ordenado',
            'remuneração', 'remuneracao', 'payment', 'subsídio', 'subsidio',
            'allowance', 'bonus', 'bónus', 'comissão', 'commission'
        ]
    }
    
    def __init__(self):
        """Initialize the categorizer"""
        self.category_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile regex patterns for each category"""
        patterns = {}
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            patterns[category] = [
                re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                for keyword in keywords
            ]
        return patterns
    
    def categorize_transaction(self, description: str, existing_category: str = None) -> str:
        """
        Categorize a single transaction based on description
        
        Args:
            description: Transaction description
            existing_category: Current category (if any)
        
        Returns:
            Category name
        """
        if not description or pd.isna(description):
            return existing_category or 'Uncategorized'
        
        description_lower = str(description).lower()
        
        # Check each category's patterns
        for category, patterns in self.category_patterns.items():
            for pattern in patterns:
                if pattern.search(description_lower):
                    return category
        
        # If no match found, keep existing or mark as uncategorized
        return existing_category if existing_category else 'Uncategorized'
    
    def categorize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize all transactions in a dataframe
        
        Args:
            df: DataFrame with 'description' and optionally 'category' columns
        
        Returns:
            DataFrame with updated 'category' column
        """
        result = df.copy()
        
        # Ensure category column exists
        if 'category' not in result.columns:
            result['category'] = 'Uncategorized'
        
        # Categorize each transaction
        result['category'] = result.apply(
            lambda row: self.categorize_transaction(
                row.get('description', ''),
                row.get('category', 'Uncategorized')
            ),
            axis=1
        )
        
        return result
    
    def analyze_spending_by_category(self, df: pd.DataFrame) -> Dict:
        """
        Analyze spending amounts by category
        
        Args:
            df: DataFrame with transactions (must have 'type', 'category', 'amount')
        
        Returns:
            Dictionary with category analysis
        """
        # Filter expenses only
        expenses = df[df['type'].str.lower() == 'expense'].copy()
        
        if len(expenses) == 0:
            return {
                'total_expenses': 0,
                'by_category': {},
                'top_categories': [],
                'summary': {}
            }
        
        # Group by category
        category_totals = expenses.groupby('category')['amount'].agg([
            ('total', 'sum'),
            ('count', 'count'),
            ('average', 'mean')
        ]).round(2)
        
        total_expenses = float(expenses['amount'].sum())
        
        # Calculate percentages
        category_totals['percentage'] = (category_totals['total'] / total_expenses * 100).round(1)
        
        # Sort by total amount
        category_totals = category_totals.sort_values('total', ascending=False)
        
        # Convert to dictionary
        by_category = {}
        for cat, row in category_totals.iterrows():
            by_category[cat] = {
                'total': float(row['total']),
                'count': int(row['count']),
                'average': float(row['average']),
                'percentage': float(row['percentage'])
            }
        
        # Top 10 categories
        top_categories = [
            {
                'category': cat,
                'amount': data['total'],
                'percentage': data['percentage']
            }
            for cat, data in list(by_category.items())[:10]
        ]
        
        # Summary statistics
        summary = {
            'total_categories': len(by_category),
            'total_transactions': int(expenses.shape[0]),
            'total_amount': float(total_expenses),
            'largest_category': category_totals.index[0] if len(category_totals) > 0 else None,
            'largest_amount': float(category_totals.iloc[0]['total']) if len(category_totals) > 0 else 0
        }
        
        return {
            'total_expenses': float(total_expenses),
            'by_category': by_category,
            'top_categories': top_categories,
            'summary': summary
        }
    
    def get_category_breakdown_report(self, df: pd.DataFrame) -> str:
        """
        Generate a text report of spending by category
        
        Args:
            df: DataFrame with transactions
        
        Returns:
            Formatted text report
        """
        analysis = self.analyze_spending_by_category(df)
        
        report = "=" * 60 + "\n"
        report += "SPENDING BREAKDOWN BY CATEGORY\n"
        report += "=" * 60 + "\n\n"
        
        report += f"Total Expenses: €{analysis['total_expenses']:,.2f}\n"
        report += f"Categories: {analysis['summary']['total_categories']}\n"
        report += f"Transactions: {analysis['summary']['total_transactions']}\n\n"
        
        report += "-" * 60 + "\n"
        report += f"{'Category':<30} {'Amount':>12} {'%':>6} {'Count':>8}\n"
        report += "-" * 60 + "\n"
        
        for cat_data in analysis['top_categories']:
            cat_info = analysis['by_category'][cat_data['category']]
            report += f"{cat_data['category']:<30} €{cat_info['total']:>10,.2f} {cat_info['percentage']:>5.1f}% {cat_info['count']:>7}\n"
        
        report += "=" * 60 + "\n"
        
        return report


def enhance_transaction_categorization(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Main function to enhance transaction categorization
    
    Args:
        df: DataFrame with transactions
    
    Returns:
        Tuple of (enhanced_df, analysis_dict)
    """
    categorizer = PortugueseTransactionCategorizer()
    
    # Categorize transactions
    enhanced_df = categorizer.categorize_dataframe(df)
    
    # Analyze spending
    analysis = categorizer.analyze_spending_by_category(enhanced_df)
    
    return enhanced_df, analysis
