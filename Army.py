import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class EuropeanArmyAnalyzer:
    def __init__(self, country_or_component):
        self.country_component = country_or_component
        self.colors = ['#0055A4', '#FF0000', '#FFCC00', '#009900', '#660099', 
                      '#FF6600', '#0066CC', '#CC0000', '#00CCCC', '#FF00FF']
        
        self.start_year = 2017  # PESCO lancé en 2017
        self.end_year = 2027
        
        # Configuration spécifique pour chaque pays/composante
        self.config = self._get_country_component_config()
        
    def _get_country_component_config(self):
        """Retourne la configuration spécifique pour chaque pays/composante"""
        configs = {
            # Pays de l'UE
            "Allemagne": {
                "type": "pays_ue",
                "budget_defense_base": 45.0,
                "personnel_base": 180000,
                "projets_pesco": 18,
                "equipements_communs": ["Eurofighter", "Leopard", "F125", "MEADS"],
                "specialisations": ["blindes", "logistique", "cyberdefense"]
            },
            "Autriche": {
                "type": "pays_ue",
                "budget_defense_base": 2.8,
                "personnel_base": 22000,
                "projets_pesco": 4,
                "equipements_communs": ["Eurofighter", "Pandur", "UH-60"],
                "specialisations": ["defense_territoriale", "neutralite"]
            },
            "Belgique": {
                "type": "pays_ue",
                "budget_defense_base": 4.5,
                "personnel_base": 25000,
                "projets_pesco": 6,
                "equipements_communs": ["F-16", "FREMM", "NH90"],
                "specialisations": ["logistique", "commandement"]
            },
            "Bulgarie": {
                "type": "pays_ue",
                "budget_defense_base": 1.2,
                "personnel_base": 31000,
                "projets_pesco": 3,
                "equipements_communs": ["MiG-29", "T-72", "Patriot"],
                "specialisations": ["defense_aerienne", "infanterie"]
            },
            "Chypre": {
                "type": "pays_ue",
                "budget_defense_base": 0.4,
                "personnel_base": 12000,
                "projets_pesco": 2,
                "equipements_communs": ["Patrol Vessels", "MANPADS"],
                "specialisations": ["surveillance_maritime", "defense_cotiere"]
            },
            "Croatie": {
                "type": "pays_ue",
                "budget_defense_base": 1.0,
                "personnel_base": 15000,
                "projets_pesco": 3,
                "equipements_communs": ["MiG-21", "Patria", "PzH2000"],
                "specialisations": ["defense_adriatique", "forces_speciales"]
            },
            "Danemark": {
                "type": "pays_ue",
                "budget_defense_base": 3.8,
                "personnel_base": 20000,
                "projets_pesco": 5,
                "equipements_communs": ["F-16", "Absalon", "Leopard"],
                "specialisations": ["marine", "operations_internationales"]
            },
            "Espagne": {
                "type": "pays_ue",
                "budget_defense_base": 18.0,
                "personnel_base": 124000,
                "projets_pesco": 10,
                "equipements_communs": ["F100", "Eurofighter", "Leopard", "NH90"],
                "specialisations": ["infanterie_marine", "patrouille_maritime", "operations_amphibies"]
            },
            "Estonie": {
                "type": "pays_ue",
                "budget_defense_base": 0.6,
                "personnel_base": 6000,
                "projets_pesco": 3,
                "equipements_communs": ["Javelin", "Patria", "Minehunters"],
                "specialisations": ["cyberdefense", "defense_balte", "guerre_electronique"]
            },
            "Finlande": {
                "type": "pays_ue",
                "budget_defense_base": 4.2,
                "personnel_base": 22000,
                "projets_pesco": 5,
                "equipements_communs": ["F-18", "Leopard", "K9"],
                "specialisations": ["artillerie", "defense_arctique", "reservistes"]
            },
            "France": {
                "type": "pays_ue",
                "budget_defense_base": 40.0,
                "personnel_base": 205000,
                "projets_pesco": 15,
                "equipements_communs": ["Rafale", "FREMM", "Leclerc", "Caesar"],
                "specialisations": ["force_nucleaire", "intervention_rapide", "renseignement"]
            },
            "Grece": {
                "type": "pays_ue",
                "budget_defense_base": 5.5,
                "personnel_base": 130000,
                "projets_pesco": 7,
                "equipements_communs": ["F-16", "Leopard", "FREMM"],
                "specialisations": ["defense_aerienne", "marine", "defense_egéenne"]
            },
            "Hongrie": {
                "type": "pays_ue",
                "budget_defense_base": 1.8,
                "personnel_base": 22500,
                "projets_pesco": 4,
                "equipements_communs": ["JAS-39", "Leopard", "PzH2000"],
                "specialisations": ["defense_centrale", "cyberdefense"]
            },
            "Irlande": {
                "type": "pays_ue",
                "budget_defense_base": 1.0,
                "personnel_base": 9000,
                "projets_pesco": 2,
                "equipements_communs": ["PC-9", "Patrol Vessels"],
                "specialisations": ["patrouille_maritime", "neutralite", "maintien_paix"]
            },
            "Italie": {
                "type": "pays_ue",
                "budget_defense_base": 25.0,
                "personnel_base": 165000,
                "projets_pesco": 12,
                "equipements_communs": ["FREMM", "Eurofighter", "Centauro", "Horizon"],
                "specialisations": ["marine", "aerospatial", "forces_speciales"]
            },
            "Lettonie": {
                "type": "pays_ue",
                "budget_defense_base": 0.7,
                "personnel_base": 5500,
                "projets_pesco": 3,
                "equipements_communs": ["Patria", "CVR(T)", "Minehunters"],
                "specialisations": ["defense_balte", "cyberdefense", "infanterie_legere"]
            },
            "Lituanie": {
                "type": "pays_ue",
                "budget_defense_base": 1.1,
                "personnel_base": 15000,
                "projets_pesco": 4,
                "equipements_communs": ["PzH2000", "Boxer", "UH-60"],
                "specialisations": ["defense_balte", "cyberdefense", "forces_rapides"]
            },
            "Luxembourg": {
                "type": "pays_ue",
                "budget_defense_base": 0.3,
                "personnel_base": 900,
                "projets_pesco": 2,
                "equipements_communs": ["A400M", "Airbus A330"],
                "specialisations": ["logistique", "transport_aerien", "cyberdefense"]
            },
            "Malte": {
                "type": "pays_ue",
                "budget_defense_base": 0.5,
                "personnel_base": 2000,
                "projets_pesco": 2,
                "equipements_communs": ["Patrol Vessels", "Helicopters"],
                "specialisations": ["surveillance_maritime", "recherche_sauvetage"]
            },
            "Pays-Bas": {
                "type": "pays_ue",
                "budget_defense_base": 11.5,
                "personnel_base": 35000,
                "projets_pesco": 8,
                "equipements_communs": ["F-35", "FREMM", "Boxer"],
                "specialisations": ["marine", "forces_speciales", "cyberdefense"]
            },
            "Pologne": {
                "type": "pays_ue",
                "budget_defense_base": 12.0,
                "personnel_base": 115000,
                "projets_pesco": 8,
                "equipements_communs": ["F-16", "Leopard", "Rosomak", "Patriot"],
                "specialisations": ["defense_territoriale", "artillerie", "forces_conventionnelles"]
            },
            "Portugal": {
                "type": "pays_ue",
                "budget_defense_base": 3.2,
                "personnel_base": 30000,
                "projets_pesco": 5,
                "equipements_communs": ["F-16", "FREMM", "Leopard"],
                "specialisations": ["marine", "patrouille_maritime", "operations_speciales"]
            },
            "Republique Tcheque": {
                "type": "pays_ue",
                "budget_defense_base": 2.5,
                "personnel_base": 24000,
                "projets_pesco": 4,
                "equipements_communs": ["JAS-39", "Pandur", "T-72"],
                "specialisations": ["defense_aerienne", "cyberdefense", "forces_rapides"]
            },
            "Roumanie": {
                "type": "pays_ue",
                "budget_defense_base": 4.2,
                "personnel_base": 70000,
                "projets_pesco": 6,
                "equipements_communs": ["F-16", "Piranha", "HIMARS"],
                "specialisations": ["defense_est", "infanterie", "defense_mer_noire"]
            },
            "Slovaquie": {
                "type": "pays_ue",
                "budget_defense_base": 1.6,
                "personnel_base": 15000,
                "projets_pesco": 3,
                "equipements_communs": ["MiG-29", "BVP", "155mm SpGH Zuzana"],
                "specialisations": ["defense_aerienne", "forces_mecanisees"]
            },
            "Slovenie": {
                "type": "pays_ue",
                "budget_defense_base": 0.6,
                "personnel_base": 7000,
                "projets_pesco": 2,
                "equipements_communs": ["Patria", "Bell 412", "Pandur"],
                "specialisations": ["defense_alpine", "forces_speciales", "cyberdefense"]
            },
            "Suede": {
                "type": "pays_ue",
                "budget_defense_base": 6.0,
                "personnel_base": 20000,
                "projets_pesco": 7,
                "equipements_communs": ["Gripen", "Visby", "Archer"],
                "specialisations": ["aerospatial", "defense_nordique", "guerre_electronique"]
            },
            # Union européenne et composantes
            "UE-27": {
                "type": "union",
                "budget_defense_base": 220.0,
                "personnel_base": 1450000,
                "projets_pesco": 60,
                "equipements_communs": ["Eurodrone", "Eurofighter", "FREMM", "MGCS", "MAWS"],
                "specialisations": ["defense_collective", "reaction_rapide", "cyberdefense", "renseignement"]
            },
            "Forces Terrestres": {
                "type": "composante",
                "personnel_base": 850000,
                "equipements_cles": ["Leopard", "Leclerc", "Puma", "Boxer", "Caesar"],
                "pays_contributeurs": ["France", "Allemagne", "Italie", "Pologne", "Espagne"]
            },
            "Forces Maritimes": {
                "type": "composante",
                "personnel_base": 250000,
                "equipements_cles": ["FREMM", "F100", "Horizon", "Type_212", "Gowind"],
                "pays_contributeurs": ["France", "Italie", "Espagne", "Allemagne", "Pays-Bas"]
            },
            "Forces Aeriennes": {
                "type": "composante",
                "personnel_base": 350000,
                "equipements_cles": ["Eurofighter", "Rafale", "F-35", "A400M", "NH90"],
                "pays_contributeurs": ["France", "Allemagne", "Italie", "Espagne", "Pologne"]
            },
            # Configuration par défaut
            "default": {
                "type": "pays_ue",
                "budget_defense_base": 8.0,
                "personnel_base": 50000,
                "projets_pesco": 4,
                "equipements_communs": ["equipement_standard"],
                "specialisations": ["defense_generique"]
            }
        }
        
        return configs.get(self.country_component, configs["default"])
    
    def generate_army_data(self):
        """Génère des données sur l'intégration des armées européennes"""
        print(f"🇪🇺 Génération des données d'intégration militaire pour {self.country_component}...")
        
        # Créer une base de données annuelle
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Annee': [date.year for date in dates]}
        
        # Données de base (uniquement pour les pays/union)
        if self.config["type"] in ["pays_ue", "union"]:
            data['Budget_Defense'] = self._simulate_defense_budget(dates)
            data['Personnel'] = self._simulate_personnel(dates)
        
        # Coopération européenne
        data['Projets_PESCO'] = self._simulate_pesco_projects(dates)
        data['Exercices_Communs'] = self._simulate_joint_exercises(dates)
        data['Interoperabilite'] = self._simulate_interoperability(dates)
        
        # Capacités opérationnelles
        data['Capacite_Projection'] = self._simulate_projection_capacity(dates)
        data['Temps_Reaction'] = self._simulate_reaction_time(dates)
        data['Equipements_Interoperables'] = self._simulate_interoperable_equipment(dates)
        
        # Efficacité et économies
        data['Economies_Echelle'] = self._simulate_economies_of_scale(dates)
        data['Reduction_Doublons'] = self._simulate_redundancy_reduction(dates)
        data['Efficacite_Operative'] = self._simulate_operational_efficiency(dates)
        
        # Indicateurs spécifiques selon le type
        if self.config["type"] in ["pays_ue", "union"]:
            for specialisation in self.config.get("specialisations", []):
                if specialisation == "cyberdefense":
                    data['Capacite_Cyber'] = self._simulate_cyber_capacity(dates)
                elif specialisation == "renseignement":
                    data['Partage_Renseignement'] = self._simulate_intelligence_sharing(dates)
                elif specialisation == "force_nucleaire":
                    data['Dissuasion_Concertée'] = self._simulate_deterrence(dates)
        
        elif self.config["type"] == "composante":
            for pays in self.config.get("pays_contributeurs", []):
                data[f'Contribution_{pays}'] = self._simulate_country_contribution(dates, pays)
        
        df = pd.DataFrame(data)
        
        # Ajouter des tendances spécifiques
        self._add_integration_trends(df)
        
        return df
    
    def _simulate_defense_budget(self, dates):
        """Simule l'évolution du budget défense"""
        base_budget = self.config["budget_defense_base"]
        
        budget = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Croissance de base différente selon le type
            if self.config["type"] == "pays_ue":
                base_growth = 0.03  # Croissance moyenne des budgets nationaux
            elif self.config["type"] == "union":
                base_growth = 0.05  # Croissance du budget européen de défense
            else:
                base_growth = 0.025
                
            # Effet de l'intégration européenne sur le budget
            integration_effect = 0.0
            if year >= 2017:  # Après le lancement de PESCO
                integration_effect = 0.01 * min(6, year - 2016)  # Effet cumulatif
                
            growth = 1 + (base_growth + integration_effect) * i
            budget.append(base_budget * growth)
        
        return budget
    
    def _simulate_personnel(self, dates):
        """Simule l'évolution des effectifs"""
        base_personnel = self.config["personnel_base"]
        
        personnel = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Effet de l'intégration européenne sur les effectifs
            integration_effect = 0.0
            if year >= 2017:
                integration_effect = 0.005 * min(5, year - 2016)
                
            # Réduction modérée des effectifs avec meilleure efficacité
            change = 1 - (0.01 - integration_effect) * i
            personnel.append(base_personnel * change)
        
        return personnel
    
    def _simulate_pesco_projects(self, dates):
        """Simule le nombre de projets PESCO"""
        projects = []
        base_projects = self.config.get("projets_pesco", 5)
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                count = 0  # Avant PESCO
            elif year < 2020:
                count = base_projects * (year - 2016) / 3  # Lancement progressif
            elif year < 2023:
                count = base_projects + 2 * (year - 2019)  # Accélération
            else:
                count = base_projects + 6 + 3 * (year - 2022)  # Maturation
                
            projects.append(count)
        
        return projects
    
    def _simulate_joint_exercises(self, dates):
        """Simule le nombre d'exercices communs"""
        exercises = []
        base_exercises = 10  # Base pour un pays moyen
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                count = base_exercises  # Avant l'intégration renforcée
            elif year < 2020:
                count = base_exercises * (1 + 0.2 * (year - 2016))  # Augmentation progressive
            elif year < 2023:
                count = base_exercises * 1.6 + 0.3 * base_exercises * (year - 2019)  # Accélération
            else:
                count = base_exercises * 2.5 + 0.4 * base_exercises * (year - 2022)  # Stabilisation
                
            # Ajustement selon le type
            if self.config["type"] in ["pays_ue", "union"]:
                multiplier = 1.0
            elif self.config["type"] == "composante":
                multiplier = 0.5
            else:
                multiplier = 0.3
                
            exercises.append(count * multiplier)
        
        return exercises
    
    def _simulate_interoperability(self, dates):
        """Simule le niveau d'interopérabilité"""
        interoperability = []
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = 45  # Faible interopérabilité avant PESCO
            elif year < 2020:
                level = 45 + 10 * (year - 2016)  # Amélioration progressive
            elif year < 2023:
                level = 75 + 8 * (year - 2019)  # Accélération
            else:
                level = 99 + 1 * (year - 2022)  # Niveau très élevé
                
            interoperability.append(min(level, 100))
        
        return interoperability
    
    def _simulate_projection_capacity(self, dates):
        """Simule la capacité de projection de force"""
        capacity = []
        base_capacity = 30  # Pourcentage de capacité base
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = base_capacity  # Capacité limitée avant intégration
            elif year < 2020:
                level = base_capacity + 8 * (year - 2016)  # Amélioration progressive
            elif year < 2023:
                level = base_capacity + 24 + 6 * (year - 2019)  # Accélération
            else:
                level = base_capacity + 42 + 4 * (year - 2022)  # Maturation
                
            capacity.append(min(level, 100))
        
        return capacity
    
    def _simulate_reaction_time(self, dates):
        """Simule le temps de réaction (en jours)"""
        reaction_time = []
        base_time = 30  # Jours pour déployer une force significative
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                days = base_time  # Temps de réaction long avant intégration
            elif year < 2020:
                days = base_time - 3 * (year - 2016)  # Réduction progressive
            elif year < 2023:
                days = base_time - 9 - 2 * (year - 2019)  # Accélération
            else:
                days = base_time - 15 - 1 * (year - 2022)  # Optimisation
                
            reaction_time.append(max(days, 5))
        
        return reaction_time
    
    def _simulate_interoperable_equipment(self, dates):
        """Simule le pourcentage d'équipements interopérables"""
        equipment = []
        base_level = 25  # Pourcentage d'équipements interopérables de base
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = base_level  # Faible interopérabilité avant intégration
            elif year < 2020:
                level = base_level + 12 * (year - 2016)  # Amélioration progressive
            elif year < 2023:
                level = base_level + 36 + 10 * (year - 2019)  # Accélération
            else:
                level = base_level + 66 + 8 * (year - 2022)  # Standardisation
                
            equipment.append(min(level, 100))
        
        return equipment
    
    def _simulate_economies_of_scale(self, dates):
        """Simule les économies d'échelle (en milliards €)"""
        economies = []
        base_savings = 0.5  # Milliards € d'économies de base
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                saving = 0  # Peu d'économies avant intégration
            elif year < 2020:
                saving = base_savings * (year - 2016)  # Économies progressives
            elif year < 2023:
                saving = base_savings * 3 + 0.8 * base_savings * (year - 2019)  # Accélération
            else:
                saving = base_savings * 5.4 + 1.2 * base_savings * (year - 2022)  # Maturation
                
            # Ajustement selon le type
            if self.config["type"] in ["pays_ue", "union"]:
                multiplier = 1.0
            elif self.config["type"] == "composante":
                multiplier = 0.7
            else:
                multiplier = 0.5
                
            economies.append(saving * multiplier)
        
        return economies
    
    def _simulate_redundancy_reduction(self, dates):
        """Simule la réduction des doublons (en %)"""
        reduction = []
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = 0  # Pas de réduction avant intégration
            elif year < 2020:
                level = 5 * (year - 2016)  # Réduction progressive
            elif year < 2023:
                level = 15 + 4 * (year - 2019)  # Accélération
            else:
                level = 27 + 3 * (year - 2022)  # Maturation
                
            reduction.append(min(level, 50))
        
        return reduction
    
    def _simulate_operational_efficiency(self, dates):
        """Simule l'efficacité opérationnelle (en %)"""
        efficiency = []
        base_efficiency = 60  # Efficacité de base
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = base_efficiency  # Efficacité modérée avant intégration
            elif year < 2020:
                level = base_efficiency + 5 * (year - 2016)  # Amélioration progressive
            elif year < 2023:
                level = base_efficiency + 15 + 4 * (year - 2019)  # Accélération
            else:
                level = base_efficiency + 27 + 3 * (year - 2022)  # Optimisation
                
            efficiency.append(min(level, 95))
        
        return efficiency
    
    def _simulate_cyber_capacity(self, dates):
        """Simule la capacité cyberdéfense"""
        capacity = []
        base_capacity = 40  # Capacité de base
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = base_capacity
            elif year < 2020:
                level = base_capacity + 8 * (year - 2016)
            elif year < 2023:
                level = base_capacity + 24 + 6 * (year - 2019)
            else:
                level = base_capacity + 42 + 4 * (year - 2022)
                
            capacity.append(min(level, 100))
        
        return capacity
    
    def _simulate_intelligence_sharing(self, dates):
        """Simule le partage de renseignement"""
        sharing = []
        base_level = 30  # Niveau de base de partage
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = base_level
            elif year < 2020:
                level = base_level + 10 * (year - 2016)
            elif year < 2023:
                level = base_level + 30 + 8 * (year - 2019)
            else:
                level = base_level + 54 + 6 * (year - 2022)
                
            sharing.append(min(level, 100))
        
        return sharing
    
    def _simulate_deterrence(self, dates):
        """Simule la dissuasion concertée"""
        deterrence = []
        base_level = 50  # Niveau de base
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = base_level
            elif year < 2020:
                level = base_level + 7 * (year - 2016)
            elif year < 2023:
                level = base_level + 21 + 5 * (year - 2019)
            else:
                level = base_level + 36 + 4 * (year - 2022)
                
            deterrence.append(min(level, 100))
        
        return deterrence
    
    def _simulate_country_contribution(self, dates, country):
        """Simule la contribution d'un pays spécifique à une composante"""
        contribution = []
        base_contribution = 15  # Pourcentage de contribution de base
        
        for i, date in enumerate(dates):
            year = date.year
            
            if year < 2017:
                level = base_contribution
            elif year < 2020:
                level = base_contribution + 2 * (year - 2016)
            elif year < 2023:
                level = base_contribution + 6 + 1.5 * (year - 2019)
            else:
                level = base_contribution + 10.5 + 1 * (year - 2022)
                
            contribution.append(min(level, 30))
        
        return contribution
    
    def _add_integration_trends(self, df):
        """Ajoute des tendances spécifiques liées à l'intégration militaire"""
        for i, row in df.iterrows():
            year = row['Annee']
            
            # Effets du lancement de PESCO (2017)
            if year >= 2017:
                df.loc[i, 'Interoperabilite'] *= 1.05  # Amélioration initiale
                df.loc[i, 'Exercices_Communs'] *= 1.10  # Augmentation initiale
            
            # Effets de la coopération renforcée (hypothétique 2020)
            if year >= 2020:
                df.loc[i, 'Capacite_Projection'] *= 1.08  # Amélioration supplémentaire
                df.loc[i, 'Efficacite_Operative'] *= 1.06  # Amélioration supplémentaire
                df.loc[i, 'Economies_Echelle'] *= 1.12  # Augmentation des économies
            
            # Impact de la pandémie COVID-19 (2020-2021)
            if 2020 <= year <= 2021:
                # Vérifier si la colonne Budget_Defense existe avant de la modifier
                if 'Budget_Defense' in df.columns:
                    df.loc[i, 'Budget_Defense'] *= 0.95  # Réduction temporaire des budgets
                df.loc[i, 'Exercices_Communs'] *= 0.80  # Réduction des exercices
            
            # Reprise post-COVID et accélération (2022-2023)
            if year >= 2022:
                df.loc[i, 'Projets_PESCO'] *= 1.15  # Accélération des projets
                df.loc[i, 'Interoperabilite'] *= 1.07  # Amélioration accélérée
    
    def create_army_analysis(self, df):
        """Crée une analyse complète de l'intégration militaire européenne"""
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Évolution des budgets et effectifs
        ax1 = plt.subplot(4, 2, 1)
        self._plot_budget_personnel(df, ax1)
        
        # 2. Coopération européenne
        ax2 = plt.subplot(4, 2, 2)
        self._plot_cooperation(df, ax2)
        
        # 3. Capacités opérationnelles
        ax3 = plt.subplot(4, 2, 3)
        self._plot_operational_capabilities(df, ax3)
        
        # 4. Interopérabilité et équipements
        ax4 = plt.subplot(4, 2, 4)
        self._plot_interoperability(df, ax4)
        
        # 5. Efficacité et économies
        ax5 = plt.subplot(4, 2, 5)
        self._plot_efficiency_economies(df, ax5)
        
        # 6. Analyse des spécialisations
        ax6 = plt.subplot(4, 2, 6)
        self._plot_specializations(df, ax6)
        
        # 7. Temps de réaction
        ax7 = plt.subplot(4, 2, 7)
        self._plot_reaction_time(df, ax7)
        
        # 8. Comparaison avant/après intégration
        ax8 = plt.subplot(4, 2, 8)
        self._plot_before_after_comparison(df, ax8)
        
        plt.suptitle(f'Analyse de l\'Intégration Militaire Européenne - {self.country_component} ({self.start_year}-{self.end_year})', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.country_component}_army_integration_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Générer les insights
        self._generate_army_insights(df)
    
    def _plot_budget_personnel(self, df, ax):
        """Plot de l'évolution des budgets et effectifs"""
        has_budget = 'Budget_Defense' in df.columns
        has_personnel = 'Personnel' in df.columns
        
        if has_budget:
            ax.plot(df['Annee'], df['Budget_Defense'], label='Budget Défense (Md€)', 
                   linewidth=2, color='#0055A4', alpha=0.8)
            ax.set_ylabel('Budget (Md€)', color='#0055A4')
            ax.tick_params(axis='y', labelcolor='#0055A4')
        
        if has_personnel:
            if has_budget:
                ax2 = ax.twinx()
            else:
                ax2 = ax
                
            ax2.plot(df['Annee'], df['Personnel'], label='Personnel', 
                    linewidth=2, color='#FF0000', alpha=0.8)
            ax2.set_ylabel('Effectifs', color='#FF0000')
            ax2.tick_params(axis='y', labelcolor='#FF0000')
        
        ax.set_title('Évolution du Budget et des Effectifs', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        if has_personnel and has_budget:
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        else:
            ax.legend(loc='upper left')
    
    def _plot_cooperation(self, df, ax):
        """Plot de la coopération européenne"""
        ax.plot(df['Annee'], df['Projets_PESCO'], label='Projets PESCO', 
               linewidth=2, color='#0055A4', alpha=0.8)
        ax.plot(df['Annee'], df['Exercices_Communs'], label='Exercices Communs', 
               linewidth=2, color='#FF0000', alpha=0.8)
        
        ax.set_title('Coopération Militaire Européenne', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nombre')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_operational_capabilities(self, df, ax):
        """Plot des capacités opérationnelles"""
        ax.plot(df['Annee'], df['Capacite_Projection'], label='Capacité de Projection (%)', 
               linewidth=2, color='#0055A4', alpha=0.8)
        ax.plot(df['Annee'], df['Efficacite_Operative'], label='Efficacité Opérative (%)', 
               linewidth=2, color='#FF0000', alpha=0.8)
        
        ax.set_title('Capacités Opérationnelles', fontsize=12, fontweight='bold')
        ax.set_ylabel('Niveau (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_interoperability(self, df, ax):
        """Plot de l'interopérabilité"""
        ax.plot(df['Annee'], df['Interoperabilite'], label='Interopérabilité (%)', 
               linewidth=2, color='#0055A4', alpha=0.8)
        ax.plot(df['Annee'], df['Equipements_Interoperables'], label='Équipements Interopérables (%)', 
               linewidth=2, color='#FF6600', alpha=0.8)
        
        ax.set_title('Interopérabilité et Standardisation', fontsize=12, fontweight='bold')
        ax.set_ylabel('Niveau (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_efficiency_economies(self, df, ax):
        """Plot de l'efficacité et des économies"""
        ax.plot(df['Annee'], df['Economies_Echelle'], label='Économies d\'Échelle (Md€)', 
               linewidth=2, color='#0055A4', alpha=0.8)
        
        ax.set_title('Efficacité et Économies', fontsize=12, fontweight='bold')
        ax.set_ylabel('Économies (Md€)', color='#0055A4')
        ax.tick_params(axis='y', labelcolor='#0055A4')
        ax.grid(True, alpha=0.3)
        
        # Réduction des doublons en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Reduction_Doublons'], label='Réduction des Doublons (%)', 
                linewidth=2, color='#009900', alpha=0.8)
        ax2.set_ylabel('Réduction (%)', color='#009900')
        ax2.tick_params(axis='y', labelcolor='#009900')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_specializations(self, df, ax):
        """Plot des spécialisations"""
        # Sélectionner les indicateurs de spécialisation disponibles
        special_columns = [col for col in df.columns if col in ['Capacite_Cyber', 'Partage_Renseignement', 'Dissuasion_Concertée']]
        
        colors = ['#0055A4', '#FF0000', '#FFCC00', '#009900', '#660099']
        
        for i, column in enumerate(special_columns):
            spec_name = column.replace('_', ' ').title()
            ax.plot(df['Annee'], df[column], label=spec_name, 
                   linewidth=2, color=colors[i % len(colors)], alpha=0.8)
        
        ax.set_title('Spécialisations et Capacités Avancées (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Niveau (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_reaction_time(self, df, ax):
        """Plot du temps de réaction"""
        ax.plot(df['Annee'], df['Temps_Reaction'], label='Temps de Réaction (jours)', 
               linewidth=2, color='#0055A4', alpha=0.8)
        
        ax.set_title('Temps de Réaction Opérationnel', fontsize=12, fontweight='bold')
        ax.set_ylabel('Jours')
        ax.invert_yaxis()  # Moins de jours = mieux
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_before_after_comparison(self, df, ax):
        """Plot de comparaison avant/après intégration"""
        # Calculer les moyennes avant et après 2017
        before_integration = df[df['Annee'] < 2017].mean()
        after_integration = df[df['Annee'] >= 2017].mean()
        
        # Sélectionner les indicateurs à comparer
        indicators = ['Interoperabilite', 'Capacite_Projection', 'Efficacite_Operative', 'Economies_Echelle']
        labels = ['Interopérabilité', 'Projection', 'Efficacité', 'Économies']
        
        before_values = [before_integration[ind] for ind in indicators]
        after_values = [after_integration[ind] for ind in indicators]
        
        x = np.arange(len(indicators))
        width = 0.35
        
        ax.bar(x - width/2, before_values, width, label='Avant 2017', color='#0055A4', alpha=0.7)
        ax.bar(x + width/2, after_values, width, label='Après 2017', color='#FF0000', alpha=0.7)
        
        ax.set_title('Comparaison Avant/Après Intégration Renforcée', fontsize=12, fontweight='bold')
        ax.set_ylabel('Valeurs moyennes')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _generate_army_insights(self, df):
        """Génère des insights analytiques sur l'intégration militaire"""
        print(f"🇪🇺 INSIGHTS ANALYTIQUES - Intégration Militaire Européenne - {self.country_component}")
        print("=" * 80)
        
        # 1. Statistiques de base
        print("\n1. 📊 IMPACT OPÉRATIONNEL:")
        interop_growth = ((df['Interoperabilite'].iloc[-1] - 
                          df['Interoperabilite'].iloc[0]) / 
                          df['Interoperabilite'].iloc[0]) * 100
        capability_growth = ((df['Capacite_Projection'].iloc[-1] - 
                             df['Capacite_Projection'].iloc[0]) / 
                             df['Capacite_Projection'].iloc[0]) * 100
        
        print(f"Amélioration de l'interopérabilité ({self.start_year}-{self.end_year}): {interop_growth:.1f}%")
        print(f"Amélioration de la capacité de projection: {capability_growth:.1f}%")
        print(f"Temps de réaction moyen: {df['Temps_Reaction'].mean():.1f} jours")
        
        # 2. Impact économique
        print("\n2. 💰 IMPACT ÉCONOMIQUE:")
        total_savings = df['Economies_Echelle'].sum()
        
        print(f"Économies d'échelle totales: {total_savings:.2f} Md€")
        print(f"Réduction moyenne des doublons: {df['Reduction_Doublons'].mean():.1f}%")
        
        # Ajouter les indicateurs spécifiques aux pays/union
        if self.config["type"] in ["pays_ue", "union"]:
            if 'Budget_Defense' in df.columns:
                budget_growth = ((df['Budget_Defense'].iloc[-1] - 
                                 df['Budget_Defense'].iloc[0]) / 
                                 df['Budget_Defense'].iloc[0]) * 100
                print(f"Croissance du budget défense: {budget_growth:.1f}%")
        
        # 3. Coopération européenne
        print("\n3. 🤝 COOPÉRATION EUROPÉENNE:")
        pesco_growth = ((df['Projets_PESCO'].iloc[-1] - 
                        df['Projets_PESCO'].iloc[0]) / 
                        df['Projets_PESCO'].iloc[0]) * 100
        exercises_growth = ((df['Exercices_Communs'].iloc[-1] - 
                           df['Exercices_Communs'].iloc[0]) / 
                           df['Exercices_Communs'].iloc[0]) * 100
        
        print(f"Augmentation des projets PESCO: {pesco_growth:.1f}%")
        print(f"Augmentation des exercices communs: {exercises_growth:.1f}%")
        
        # 4. Spécificités du pays/composante
        print(f"\n4. 🌟 SPÉCIFICITÉS DE {self.country_component.upper()}:")
        print(f"Type: {self.config['type']}")
        if self.config["type"] in ["pays_ue", "union"]:
            print(f"Spécialisations: {', '.join(self.config.get('specialisations', []))}")
            print(f"Équipements communs: {', '.join(self.config.get('equipements_communs', []))}")
        elif self.config["type"] == "composante":
            print(f"Pays contributeurs: {', '.join(self.config.get('pays_contributeurs', []))}")
            print(f"Équipements clés: {', '.join(self.config.get('equipements_cles', []))}")
        
        # 5. Événements marquants
        print("\n5. 📅 ÉVÉNEMENTS MARQUANTS:")
        print("• 2017: Lancement de PESCO (Coopération structurée permanente)")
        print("• 2017-2019: Mise en place des premiers projets communs")
        print("• 2020: Impact de la pandémie COVID-19 sur les exercices")
        print("• 2021-2022: Reprise et accélération de l'intégration")
        print("• 2023-2027: Plein effet des projets et maturation des capacités")
        
        # 6. Recommandations stratégiques
        print("\n6. 💡 RECOMMANDATIONS STRATÉGIQUES:")
        if self.config["type"] in ["pays_ue", "union"]:
            print("• Poursuivre l'harmonisation des équipements et doctrines")
            print("• Développer les capacités de projection communes")
            print("• Renforcer la coopération en matière de cyberdéfense")
            print("• Augmenter les exercices interarmées multinationaux")
        elif self.config["type"] == "composante":
            print("• Standardiser les équipements et procédures")
            print("• Développer des centres d'excellence spécialisés")
            print("• Renforcer l'interopérabilité des systèmes de commandement")
            print("• Créer des brigades multinationales permanentes")
        
        # Recommandations spécifiques selon les spécialisations
        if self.config["type"] in ["pays_ue", "union"] and "cyberdefense" in self.config.get("specialisations", []):
            print("• Développer un commandement cyber européen intégré")
            print("• Investir dans la formation et le recrutement de experts cyber")
        if self.config["type"] in ["pays_ue", "union"] and "renseignement" in self.config.get("specialisations", []):
            print("• Renforcer le partage du renseignement en temps réel")
            print("• Créer des centres d'analyse communs")
        if self.config["type"] in ["pays_ue", "union"] and "force_nucleaire" in self.config.get("specialisations", []):
            print("• Développer une doctrine de dissuasion concertée")
            print("• Renforcer le dialogue stratégique européen")

def main():
    """Fonction principale pour l'analyse de l'intégration militaire européenne"""
    # Liste des pays et composantes à analyser
    options = [
        "Allemagne", "Autriche", "Belgique", "Bulgarie", "Chypre", "Croatie", "Danemark", "Espagne",
        "Estonie", "Finlande", "France", "Grece", "Hongrie", "Irlande", "Italie", "Lettonie", "Lituanie",
        "Luxembourg", "Malte", "Pays-Bas", "Pologne", "Portugal", "Republique Tcheque", "Roumanie",
        "Slovaquie", "Slovenie", "Suede", "UE-27", "Forces Terrestres", "Forces Maritimes", "Forces Aeriennes"
    ]
    
    print("🇪🇺 ANALYSE DE L'INTÉGRATION MILITAIRE EUROPÉENNE (2017-2027)")
    print("=" * 70)
    
    # Demander à l'utilisateur de choisir un pays/composante
    print("Options disponibles:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    try:
        choix = int(input("\nChoisissez le numéro du pays/composante à analyser: "))
        if choix < 1 or choix > len(options):
            raise ValueError
        option_selectionnee = options[choix-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection de l'UE-27 par défaut.")
        option_selectionnee = "UE-27"
    
    # Initialiser l'analyseur
    analyzer = EuropeanArmyAnalyzer(option_selectionnee)
    
    # Générer les données
    army_data = analyzer.generate_army_data()
    
    # Sauvegarder les données
    output_file = f'{option_selectionnee}_army_integration_data_2017_2027.csv'
    army_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print("\n👀 Aperçu des données:")
    print(army_data[['Annee', 'Interoperabilite', 'Capacite_Projection', 
                    'Projets_PESCO', 'Economies_Echelle']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse d'intégration militaire...")
    analyzer.create_army_analysis(army_data)
    
    print(f"\n✅ Analyse pour {option_selectionnee} terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year}")
    print("📦 Données: Coopération, capacités, interopérabilité, économies")

if __name__ == "__main__":
    main()