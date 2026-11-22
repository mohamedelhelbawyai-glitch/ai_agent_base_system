---
name: prisma-conventions
description: Standards Prisma et base de données. Use when "prisma", "database", "schema", "migration", "query".
allowed-tools: Read, Grep, Glob, Bash
---

# Prisma Conventions

## Purpose
Standards pour utiliser Prisma dans le projet consultant-manager.

## Architecture Base de Données

### Modèles Principaux

```prisma
model Consultant {
  id              String   @id @default(uuid())
  nom             String
  prenom          String
  email           String   @unique
  telephone       String?
  competences     String   // JSON array
  tjm             Float
  statut          String   @default("DISPONIBLE")
  dateCreation    DateTime @default(now())
  dateModification DateTime @updatedAt

  missions        Mission[]
}

model Mission {
  id                   String   @id @default(uuid())
  consultantId         String
  nomClient            String
  lieu                 String?
  dateDebut            DateTime
  dateFin              DateTime
  tjmApplique          Float
  description          String?
  competencesUtilisees String?  // JSON array
  statutFacturation    String   @default("EN_ATTENTE")
  dateCreation         DateTime @default(now())
  dateModification     DateTime @updatedAt

  consultant           Consultant @relation(fields: [consultantId], references: [id], onDelete: Cascade)

  @@index([consultantId])
  @@index([dateDebut, dateFin])
}
```

### Principes de Design

1. **UUIDs pour les IDs**: Plus sûrs que les auto-increment
2. **Timestamps automatiques**: `@default(now())` et `@updatedAt`
3. **Nullable approprié**: `?` uniquement si vraiment optionnel
4. **Indexes stratégiques**: Sur foreign keys et champs de recherche
5. **Cascade Delete**: Missions supprimées si consultant supprimé

## Migrations

### Créer une Migration

```bash
cd backend
npx prisma migrate dev --name description_du_changement
```

**Conventions de nommage:**
- `init` - Migration initiale
- `add_field_name` - Ajout d'un champ
- `rename_field_x_to_y` - Renommage
- `add_table_name` - Nouvelle table
- `create_index_on_field` - Nouvel index

### Workflow de Migration

```bash
# 1. Modifier schema.prisma
# 2. Créer la migration
npx prisma migrate dev --name add_consultant_photo

# 3. Regénérer le client
npx prisma generate

# 4. Vérifier que tout compile
npm run build
```

### Migration en Production

```bash
# Appliquer les migrations en prod
npx prisma migrate deploy

# Seed la base si nécessaire
npx prisma db seed
```

## Queries Prisma

### CRUD de Base

```typescript
// CREATE
const consultant = await prisma.consultant.create({
  data: {
    nom: 'Dupont',
    prenom: 'Jean',
    email: 'jean@example.com',
    competences: JSON.stringify(['React', 'TypeScript']),
    tjm: 500,
    statut: 'DISPONIBLE'
  }
});

// READ avec relations
const consultant = await prisma.consultant.findUnique({
  where: { id: consultantId },
  include: {
    missions: {
      orderBy: { dateDebut: 'desc' }
    }
  }
});

// READ liste avec filtres
const consultants = await prisma.consultant.findMany({
  where: {
    statut: 'DISPONIBLE',
    email: { contains: '@example.com' }
  },
  orderBy: { nom: 'asc' }
});

// UPDATE
const updated = await prisma.consultant.update({
  where: { id: consultantId },
  data: { tjm: 550 }
});

// DELETE
await prisma.consultant.delete({
  where: { id: consultantId }
});
```

### Queries Complexes

**Filtres avancés:**
```typescript
// Consultants avec missions actives
const consultantsEnMission = await prisma.consultant.findMany({
  where: {
    missions: {
      some: {
        dateDebut: { lte: new Date() },
        dateFin: { gte: new Date() }
      }
    }
  },
  include: { missions: true }
});

// Missions se terminant bientôt
const in30Days = new Date();
in30Days.setDate(in30Days.getDate() + 30);

const missionsEndingSoon = await prisma.mission.findMany({
  where: {
    dateFin: {
      gte: new Date(),
      lte: in30Days
    }
  },
  include: { consultant: true }
});
```

**Aggregations:**
```typescript
// Compter les consultants par statut
const stats = await prisma.consultant.groupBy({
  by: ['statut'],
  _count: true
});

// Revenus totaux
const totalRevenue = await prisma.mission.aggregate({
  _sum: {
    tjmApplique: true
  },
  where: {
    statutFacturation: 'PAYEE'
  }
});
```

**Transactions:**
```typescript
// Créer consultant et mission en une transaction
const result = await prisma.$transaction(async (tx) => {
  const consultant = await tx.consultant.create({
    data: { /* ... */ }
  });

  const mission = await tx.mission.create({
    data: {
      consultantId: consultant.id,
      /* ... */
    }
  });

  return { consultant, mission };
});
```

## Patterns Spécifiques au Projet

### Gestion des JSON Fields

**Competences (array):**
```typescript
// Écriture
await prisma.consultant.create({
  data: {
    competences: JSON.stringify(['React', 'Node.js'])
  }
});

// Lecture
const consultant = await prisma.consultant.findUnique({ where: { id } });
const competences: string[] = JSON.parse(consultant.competences);
```

### Calcul du Statut Consultant

```typescript
interface ConsultantWithMissions {
  missions: Mission[];
  statut: string;
}

async function getConsultantWithRealStatus(id: string) {
  const consultant = await prisma.consultant.findUnique({
    where: { id },
    include: {
      missions: {
        where: {
          dateDebut: { lte: new Date() },
          dateFin: { gte: new Date() }
        }
      }
    }
  });

  // Si mission active, forcer EN_MISSION
  const hasActiveMission = consultant.missions.length > 0;
  return {
    ...consultant,
    statut: hasActiveMission ? 'EN_MISSION' : consultant.statut
  };
}
```

### Queries Optimisées

**❌ N+1 Problem:**
```typescript
// Mauvais: N+1 queries
const consultants = await prisma.consultant.findMany();
for (const consultant of consultants) {
  const missions = await prisma.mission.findMany({
    where: { consultantId: consultant.id }
  });
}
```

**✅ Solution: Include:**
```typescript
// Bon: 1 seule query
const consultants = await prisma.consultant.findMany({
  include: { missions: true }
});
```

**Pagination:**
```typescript
const page = 1;
const pageSize = 20;

const consultants = await prisma.consultant.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: { nom: 'asc' }
});

const total = await prisma.consultant.count();
```

## Prisma Studio

### Ouvrir l'Interface Graphique
```bash
cd backend
npx prisma studio
```

Ouvre un navigateur sur http://localhost:5555 pour:
- Visualiser les données
- Créer/Modifier/Supprimer des enregistrements
- Tester les relations
- Inspecter le schéma

## Seed Data

### Créer un Seed Script

```typescript
// backend/prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Nettoyer
  await prisma.mission.deleteMany();
  await prisma.consultant.deleteMany();

  // Créer des données de test
  const consultant1 = await prisma.consultant.create({
    data: {
      nom: 'Dupont',
      prenom: 'Jean',
      email: 'jean.dupont@example.com',
      competences: JSON.stringify(['React', 'TypeScript', 'Node.js']),
      tjm: 500,
      statut: 'DISPONIBLE'
    }
  });

  const consultant2 = await prisma.consultant.create({
    data: {
      nom: 'Martin',
      prenom: 'Marie',
      email: 'marie.martin@example.com',
      competences: JSON.stringify(['Python', 'Django', 'PostgreSQL']),
      tjm: 450,
      statut: 'DISPONIBLE'
    }
  });

  // Créer une mission active
  await prisma.mission.create({
    data: {
      consultantId: consultant1.id,
      nomClient: 'Acme Corp',
      lieu: 'Paris',
      dateDebut: new Date('2026-01-01'),
      dateFin: new Date('2026-06-30'),
      tjmApplique: 500,
      description: 'Développement application React',
      competencesUtilisees: JSON.stringify(['React', 'TypeScript']),
      statutFacturation: 'EN_ATTENTE'
    }
  });

  console.log('✅ Seed completed');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

**Configurer dans package.json:**
```json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

**Exécuter:**
```bash
npx prisma db seed
```

## Bonnes Pratiques

### Toujours Déconnecter
```typescript
// À la fin du script ou au shutdown
await prisma.$disconnect();
```

### Gérer les Erreurs
```typescript
try {
  const consultant = await prisma.consultant.create({ data });
} catch (error) {
  if (error.code === 'P2002') {
    // Unique constraint violation
    throw new Error('Email déjà utilisé');
  }
  throw error;
}
```

### Utiliser les Types Générés
```typescript
import { Consultant, Mission, Prisma } from '@prisma/client';

// Type avec relations
type ConsultantWithMissions = Prisma.ConsultantGetPayload<{
  include: { missions: true }
}>;
```

## Checklist

Avant de commiter des changements Prisma:
- [ ] Migration créée avec nom descriptif
- [ ] `prisma generate` exécuté
- [ ] Schema valide (pas d'erreurs de compilation)
- [ ] Indexes ajoutés sur foreign keys
- [ ] Timestamps (`dateCreation`, `dateModification`) présents
- [ ] Cascade delete configuré si approprié
- [ ] Types TypeScript régénérés
- [ ] Tests mis à jour si schéma changé
- [ ] Seed data mis à jour si nécessaire

## Commandes Utiles

```bash
# Ouvrir Prisma Studio
npx prisma studio

# Générer le client Prisma
npx prisma generate

# Créer et appliquer une migration
npx prisma migrate dev --name my_migration

# Appliquer migrations en prod
npx prisma migrate deploy

# Réinitialiser la base (dev only!)
npx prisma migrate reset

# Formater le schema
npx prisma format

# Valider le schema
npx prisma validate

# Seed la base
npx prisma db seed
```

## Ressources

- [Prisma Documentation](https://www.prisma.io/docs)
- [Prisma Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)
- [Prisma Client API](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
